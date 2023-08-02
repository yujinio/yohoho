from typing import Union

from fastapi import FastAPI, status, Response, Request

from fastapi.middleware.cors import CORSMiddleware

import nkinopoiskpy

from nkinopoiskpy.movie import Movie

import json
import logging
import sys

from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.search_by_keyword_request import SearchByKeywordRequest
from kinopoisk_unofficial.model.dictonary.film_type import FilmType
from kinopoisk_unofficial.request.films.film_request import FilmRequest

logging.basicConfig(
    filename=('kino_server_int.log'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search/{query}")
def search(query: str, request: Request):
    try:
        logger.info(request.client.host + ', ' + query)
        api_client = KinopoiskApiClient("token")
        api_request = SearchByKeywordRequest(query)
        response = api_client.films.send_search_by_keyword_request(api_request)
        movies = []
        if query.isdigit():
            try:
                request_by_id = FilmRequest(int(query))
                response_by_id = api_client.films.send_film_request(request_by_id)
                name = ''
                film_by_id = response_by_id.film
                if film_by_id.name_ru is None:
                    name=film_by_id.name_en
                else:
                    name=film_by_id.name_ru
                movies.append({"id":film_by_id.kinopoisk_id, "title":name + ' (' + str(film_by_id.year) + ') ' + film_by_id.type.name, "poster":film_by_id.poster_url_preview})
            except Exception as error:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error('Film by id error: ' + str(error) + ", line: " + str(exc_tb.tb_lineno))
                pass
        for film in response.films:
             if film.year is None or film.year == 'None' or film.year == 'null':
                 continue
             movie_type = ''
             name = ''
             if film.name_ru is None:
                 name=film.name_en
             else:
                 name=film.name_ru
             movies.append({"id":film.film_id, "title":name + ' (' + str(film.year) + ') ' + film.type.name, "poster":film.poster_url_preview})
        json_string = json.dumps(movies)
        logger.info(request.client.host + ', result_json: ' + json.dumps(movies, ensure_ascii=False))
        if len(movies) == 0:
            return []
        return Response(content=json_string, media_type="application/json")
    except Exception as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error('Error: ' + str(error) + ", line: " + str(exc_tb.tb_lineno))
        try:
            logger.info('Try official API')
            movie_list = Movie.objects.search(query)
            if len(movie_list) == 0:
                return []
            movies = []
            for movie in movie_list:
                 if movie.runtime is None:
                     continue
                 if movie.year is None or movie.year == 'None':
                     continue
                 movie_type = ''
                 if movie.series:
                     movie_type='Сериал'
                 else:
                     movie_type='Фильм'
                 movies.append({"id":movie.id, "title":movie.title + ' (' + str(movie.year) + ') ' + movie_type})
            json_string = json.dumps(movies)
            logger.info(request.client.host + ', result_json: ' + json.dumps(movies, ensure_ascii=False))
            return Response(content=json_string, media_type="application/json")
        except Exception as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error('Error: ' + str(error) + ", line: " + str(exc_tb.tb_lineno))
            return []
