<template>
  <n-config-provider :theme="darkTheme" inline-theme-disabled>
    <n-layout position="absolute">
      <n-layout-header bordered position="static">
        <n-card embedded>
          <Nav />
        </n-card>
      </n-layout-header>

      <n-layout-content content-style="padding-top: 25px" bordered position="static">
        <n-message-provider>
          <n-loading-bar-provider>
            <RouterView />
          </n-loading-bar-provider>
        </n-message-provider>
      </n-layout-content>
    </n-layout>
  </n-config-provider>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import Nav from '@/components/Nav.vue'
import {
  NLayout,
  NLayoutContent,
  NLayoutHeader,
  NMessageProvider,
  NCard,
  NConfigProvider,
  NLoadingBarProvider,
  darkTheme
} from 'naive-ui'
</script>
