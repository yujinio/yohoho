<template>
  <n-space>
    <n-icon size="40">
      <svg
        version="1.0"
        xmlns="http://www.w3.org/2000/svg"
        width="16.000000pt"
        height="16.000000pt"
        viewBox="0 0 16.000000 16.000000"
        preserveAspectRatio="xMidYMid meet"
      >
        <g
          transform="translate(0.000000,16.000000) scale(0.006154,-0.006154)"
          fill="#000000"
          stroke="none"
        >
          <path
            d="M0 1300 l0 -1300 1300 0 1300 0 0 1300 0 1300 -1300 0 -1300 0 0
-1300z m715 478 c60 -134 120 -267 133 -296 l24 -52 92 187 c71 144 202 381
220 400 1 1 29 -6 61 -17 38 -12 59 -23 57 -32 -12 -55 -194 -440 -283 -598
l-65 -115 6 -265 c3 -146 4 -267 2 -270 -2 -3 -43 -5 -92 -5 -49 0 -90 2 -92
5 -3 3 -1 124 2 270 l7 265 -62 125 c-35 69 -77 157 -94 197 -48 111 -171 415
-171 424 0 7 24 10 121 17 24 2 31 -12 134 -240z m1081 -133 c93 -46 186 -175
225 -315 19 -69 17 -262 -4 -340 -46 -169 -121 -267 -235 -310 -70 -27 -128
-22 -210 15 -182 83 -262 288 -218 555 39 232 110 366 221 417 46 21 156 10
221 -22z"
          />
          <path
            d="M1619 1529 c-27 -27 -62 -106 -85 -194 -13 -50 -18 -108 -18 -205 -1
-123 1 -139 22 -180 104 -199 268 -140 328 118 46 195 -16 402 -138 461 -56
27 -82 27 -109 0z"
          />
        </g>
      </svg>
    </n-icon>
    <n-menu :options="menuOptions" mode="horizontal" />
  </n-space>
</template>

<script setup lang="ts">
import { h } from 'vue'
import { RouterLink } from 'vue-router'
import { NIcon, NMenu, NSpace } from 'naive-ui'
import type { MenuOption } from 'naive-ui'
import { LogoGithub } from '@vicons/ionicons5'

const menuOptions: MenuOption[] = [
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            name: 'main',
            path: '/'
          }
        },
        { default: () => 'На главную' }
      ),
    key: 'go-main'
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            name: 'about',
            path: '/about'
          }
        },
        { default: () => 'О сервисе' }
      ),
    key: 'go-about'
  },
  {
    label: () =>
      h(
        'a',
        {
          href: 'https://github.com/yujinio/yohoho',
          target: '_blank',
          rel: 'noopener noreferrer'
        },
        { default: () => '' }
      ),
    key: 'go-source-code',
    icon: () => h(LogoGithub)
  }
]
</script>
