<template>
  <main>
    <n-layout>
      <n-layout-content>
        <n-grid cols="7" item-responsive responsive="screen" x-gap="24" y-gap="24">
          <n-gi span="7 m:5 l:5" offset="0 m:1 l:1">
            <n-card v-if="iframes.length > 0" closable @close="resetMovieSearch">
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
            <n-card v-if="iframes.length === 0">
              <n-tabs type="segment">
                <n-tab-pane name="По названию фильма">
                  <n-auto-complete
                    :input-props="{ autocomplete: 'disabled' }"
                    :options="movieSearchOptions"
                    :loading="movieSearchLoading"
                    placeholder="Как я встретил вашу маму"
                    v-model:value="movieSearchValue"
                    size="large"
                    @update:value="updateMovieSearchOptions"
                    @select="getMovieByKinopoiskId"
                  />
                </n-tab-pane>
                <n-tab-pane name="По ID на Кинопоиске">
                  <n-input
                    :loading="getMovieByKinopoiskIdDelayedLoading"
                    size="large"
                    type="text"
                    placeholder="12345"
                    @update:value="getMovieByKinopoiskIdDelayed"
                  />
                </n-tab-pane>
              </n-tabs>
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
  NInput,
  useMessage,
  useLoadingBar
} from 'naive-ui'
import { ref } from 'vue'
import axios from 'axios'

const BASE_BACKEND_SERVER_URL = import.meta.env.VITE_BASE_API_SERVER_URL

const iframes = ref([])
const getMovieByKinopoiskIdTimeout = ref(0)
const movieSearchTimeout = ref(0)
const movieSearchValue = ref('')
const movieSearchOptions = ref([])
const movieSearchLoading = ref(false)
const getMovieByKinopoiskIdDelayedLoading = ref(false)
const movieLoadingBar = useLoadingBar()
const message = useMessage()

const resetMovieSearch = () => {
  iframes.value = []
  clearTimeout(movieSearchTimeout.value)
  movieSearchValue.value = ''
  movieSearchOptions.value = []
  movieSearchLoading.value = false
}

const getMovieByKinopoiskId = async (kinopoiskId: string | number) => {
  if (kinopoiskId === '' || kinopoiskId === null || kinopoiskId === undefined) {
    message.error(
      'Сперва нужно ввести ID или выбрать фильм из предложенных при автоматическом поиске!',
      { keepAliveOnHover: true, closable: true, duration: 5000 }
    )
    return
  }

  if (typeof kinopoiskId === 'string') kinopoiskId = parseInt(kinopoiskId)

  movieLoadingBar.start()
  iframes.value = await getIframes(kinopoiskId)
  if (iframes.value.length > 0) {
    movieLoadingBar.finish()
  } else {
    message.error('По вашему запросу ничего не найдено :(', {
      keepAliveOnHover: true,
      closable: true,
      duration: 5000
    })
    movieLoadingBar.error()
  }
}

const getMovieByKinopoiskIdDelayed = async (kinopoiskId: string | number) => {
  if (getMovieByKinopoiskIdTimeout.value) clearTimeout(getMovieByKinopoiskIdTimeout.value)
  if (!getMovieByKinopoiskIdDelayedLoading.value) getMovieByKinopoiskIdDelayedLoading.value = true

  getMovieByKinopoiskIdTimeout.value = setTimeout(async () => {
    await getMovieByKinopoiskId(kinopoiskId)
    getMovieByKinopoiskIdDelayedLoading.value = false
  }, 2500)
}

const updateMovieSearchOptions = async (value: string) => {
  if (movieSearchTimeout.value) clearTimeout(movieSearchTimeout.value)
  if (value === '' || value === null || value === undefined) {
    movieSearchLoading.value = false
    return
  }
  if (!movieSearchLoading.value) movieSearchLoading.value = true
  movieSearchTimeout.value = setTimeout(async () => {
    movieSearchOptions.value = await getMovieOptions(value)
    if (movieSearchOptions.value.length === 0) {
      message.error('По вашему запросу ничего не найдено :(', {
        keepAliveOnHover: true,
        closable: true,
        duration: 5000
      })
    }
    movieSearchLoading.value = false
  }, 1500)
}

const getIframes = async (kinopoiskId: number) => {
  try {
    const response = await axios.get(`${BASE_BACKEND_SERVER_URL}/api/iframes`, {
      params: { kinopoisk_id: kinopoiskId }
    })
    return response.data
  } catch (error) {
    console.log(error)
  }
  return []
}

const getMovieOptions = async (query: string) => {
  try {
    const response = await axios.get(`${BASE_BACKEND_SERVER_URL}/api/search`, {
      params: { q: query }
    })
    return response.data.map((movie: { kinopoisk_id: number; title: string }) => {
      return {
        label: movie.title,
        value: movie.kinopoisk_id
      }
    })
  } catch (error) {
    console.log(error)
  }
  return []
}
</script>
