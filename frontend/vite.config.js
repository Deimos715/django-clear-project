import { defineConfig } from 'vite';
import path from 'path';
import copy from 'rollup-plugin-copy';

export default defineConfig({
  base: './', //базовый путь проекта, что означает, что все ссылки на ресурсы в проекте будут относительными
  plugins: [
    copy({
      targets: [
        { src: 'src/fonts/*', dest: 'dist/assets/fonts' },
        { src: 'src/img/*', dest: 'dist/assets/img' },

      ],
      hook: 'writeBundle'
    })
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '@img': path.resolve(__dirname, 'src/img'),
    }
  },
  build: {
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'index.html'),
        exemple: path.resolve(__dirname, 'exemple.html')
      },
      output: {
        assetFileNames: (assetInfo) => {
          const extType = assetInfo.name.split('.').pop();
          if (/ttf|otf|woff|woff2/i.test(extType)) {
            return 'assets/fonts/[name][extname]';
          }
          if (/css/i.test(extType)) {
            return 'assets/css/[name]-[hash].min.css';
          }
          if (/png|jpe?g|gif|svg|webp/i.test(extType)) {
            return 'assets/img/[name][extname]';
          }
          return 'assets/img/[name]-[hash][extname]';
        },
        chunkFileNames: 'assets/js/[name]-[hash].js', //Для 2-х и более страниц
        // entryFileNames: 'assets/js/[name]-[hash].js', //Для одной страницы
      }
    }
  },
});
