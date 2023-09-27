<template>
  <main>
    <n-layout>
      <n-layout-content>
        <n-grid cols="7" item-responsive responsive="screen" x-gap="24" y-gap="24">
          <n-gi span="7 m:5 l:5" offset="0 m:1 l:1">
            <n-card v-if="iframes.length > 0" id="movieCard">
              <n-tabs type="segment">
                <n-tab-pane
                  v-for="iframe in iframes"
                  :name="iframe['source_name']"
                  :tab="iframe['source_name']"
                >
                  <iframe
                    :src="iframe['iframe_url']"
                    width="100%"
                    height="360"
                    frameborder="0"
                    allowfullscreen
                  />
                </n-tab-pane>
              </n-tabs>
            </n-card>
          </n-gi>

          <n-gi span="7 m:5 l:3" offset="0 m:1 l:2">
            <n-card>
              <n-grid cols="7" item-responsive responsive="screen" x-gap="12" y-gap="12">
                <n-gi span="7 m:6 l:6">
                  <n-auto-complete
                    :input-props="{ autocomplete: 'disabled' }"
                    :options="searchOptions"
                    :loading="searchOptionsLoading"
                    placeholder="Название фильма или его ID на Кинопоиске"
                    v-model:value="searchValue"
                    size="large"
                    @update:value="updateSearchResults"
                    @select="setMovieId"
                  />
                </n-gi>

                <n-gi span="2 m:1 l:1" offset="3 m:0 l:0">
                  <n-button size="large" @click="searchMovie">Поиск</n-button>
                </n-gi>
              </n-grid>
            </n-card>
          </n-gi>
        </n-grid>
      </n-layout-content>
    </n-layout>
  </main>
</template>

<script setup lang="ts">
import {
  NLayout,
  NAutoComplete,
  NCard,
  NLayoutContent,
  NGrid,
  NGi,
  NTabPane,
  NTabs,
  NButton,
  useMessage,
  useLoadingBar
} from 'naive-ui'
import { ref } from 'vue'
import axios from 'axios'

const BASE_BACKEND_SERVER_URL = import.meta.env.VITE_BASE_API_SERVER_URL

const iframes = ref([])
const movieId = ref()
const searchValue = ref('')
const searchOptions = ref([])
const searchOptionsLoading = ref(false)
const searchTimeout = ref(0)
const loadingBar = useLoadingBar()
const message = useMessage()

const searchMovie = async () => {
  if (searchOptionsLoading.value) searchOptionsLoading.value = false
  if (movieId.value === '' || movieId.value === null || movieId.value === undefined) {
    message.error(
      'Сперва нужно ввести ID или выбрать фильм из предложенных при автоматическом поиске!',
      { keepAliveOnHover: true, closable: true, duration: 5000 }
    )
    return
  }
  loadingBar.start()
  iframes.value = await getIframes(movieId.value)
  if (iframes.value.length > 0) {
    loadingBar.finish()
  } else {
    message.error('По вашему запросу ничего не найдено :(', {
      keepAliveOnHover: true,
      closable: true,
      duration: 5000
    })
    loadingBar.error()

    movieId.value = null
  }
}

const setMovieId = (value: string | number) => {
  if (searchOptionsLoading.value) searchOptionsLoading.value = false
  movieId.value = typeof value === 'string' ? parseInt(value) : value
}

const updateSearchResults = async () => {
  if (searchTimeout.value) clearTimeout(searchTimeout.value)
  if (!isNaN(parseInt(searchValue.value))) {
    setMovieId(searchValue.value)
    return
  }
  if (!searchOptionsLoading.value) searchOptionsLoading.value = true
  searchTimeout.value = setTimeout(async () => {
    var movies = []
    try {
      const response = await axios.get(`${BASE_BACKEND_SERVER_URL}/search`, {
        params: { q: searchValue.value }
      })
      movies = response.data
    } catch (error) {
      console.log(error)
    }
    if (movies.length === 0)
      message.error('По вашему запросу ничего не найдено :(', {
        keepAliveOnHover: true,
        closable: true,
        duration: 5000
      })
    searchOptions.value = movies.map((movie: { kinopoisk_id: number; title: string }) => {
      return {
        label: movie.title,
        value: movie.kinopoisk_id
      }
    })
    searchOptionsLoading.value = false
  }, 1500)
}

const getIframes = async (kinopoiskId: number) => {
  try {
    const response = await axios.get(`${BASE_BACKEND_SERVER_URL}/iframes`, {
      params: { kinopoisk_id: kinopoiskId }
    })
    return response.data
  } catch (error) {
    console.log(error)
  }
  return []
}
</script>
