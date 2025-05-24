import { src, dest, watch, parallel, series } from "gulp";
import sass from "gulp-sass";
import * as sassCompiler from "sass";
import concat from "gulp-concat";
import uglify from "gulp-uglify";
import browserSync from "browser-sync";
import autoprefixer from "gulp-autoprefixer";
import clean from "gulp-clean";
import webp from "gulp-webp";
import imagemin from "gulp-imagemin";
import newer from "gulp-newer";
import avif from "gulp-avif";
import ttf2woff2 from "gulp-ttf2woff2";
import ttf2woff from "gulp-ttf2woff";
import svgSprite from "gulp-svg-sprite";
import include from "gulp-include";
import cleanCSS from "gulp-clean-css";
import webpack from "webpack";
import webpackStream from "webpack-stream";
import rev from "gulp-rev";
import revReplace from "gulp-rev-replace";
import replace from "gulp-replace";

const scss = sass(sassCompiler);

// Обработка страниц
function pages() {
  return src("app/pages/*.html")
    .pipe(
      include({
        includePaths: "app/components",
      })
    )
    .pipe(replace(/\n\s*\n/g, "\n")) // Удаление лишних строк
    .pipe(dest("app"))
    .pipe(browserSync.stream());
}

// Обработка шрифтов
// Dev
function fontsWoff() {
  return src("app/fonts/src/*.ttf", { encoding: false })
    .pipe(ttf2woff())
    .pipe(dest("app/fonts"));
}

function fontsWoff2() {
  return src("app/fonts/src/*.ttf", { encoding: false })
    .pipe(ttf2woff2())
    .pipe(dest("app/fonts"));
}

const fonts = parallel(fontsWoff, fontsWoff2);

// Prod
function fontsBuildWoff() {
  return src("app/fonts/src/*.ttf", { encoding: false })
    .pipe(ttf2woff())
    .pipe(dest("dist/fonts"));
}

function fontsBuildWoff2() {
  return src("app/fonts/src/*.ttf", { encoding: false })
    .pipe(ttf2woff2())
    .pipe(dest("dist/fonts"));
}

const fontsBuild = parallel(fontsBuildWoff, fontsBuildWoff2);

// Обработка шрифтов Fontawesome
// Dev
function copyFontAwesome() {
  return src("node_modules/@fortawesome/fontawesome-free/webfonts/*", {
    encoding: false,
  }).pipe(dest("app/fonts"));
}

// Prod
function copyFontAwesomeBuild() {
  return src("node_modules/@fortawesome/fontawesome-free/webfonts/*", {
    encoding: false,
  }).pipe(dest("dist/fonts"));
}

// Обработка изображений
// Dev
function images() {
  // Обрабатываем все изображения (кроме SVG) и конвертируем в WebP
  src(["app/images/src/*.*", "!app/images/src/*.svg"], { encoding: false })
    .pipe(newer("app/images"))
    .pipe(webp())
    .pipe(dest("app/images"));

  // Обрабатываем все изображения (кроме SVG) и конвертируем в AVIF
  src(["app/images/src/*.*", "!app/images/src/*.svg"], { encoding: false })
    .pipe(newer("app/images"))
    .pipe(avif({ quality: 50 }))
    .pipe(dest("app/images"));

  // Обрабатываем все изображения (включая SVG) с использованием imagemin
  return src("app/images/src/*.*", { encoding: false })
    .pipe(newer("app/images"))
    .pipe(imagemin())
    .pipe(dest("app/images"));
}

// Prod
function imagesBuild() {
  // Обрабатываем все изображения (кроме SVG) и конвертируем в WebP
  src(["app/images/src/*.*", "!app/images/src/*.svg"], { encoding: false })
    .pipe(newer("dist/images"))
    .pipe(webp())
    .pipe(dest("dist/images"));

  // Обрабатываем все изображения (кроме SVG) и конвертируем в AVIF
  src(["app/images/src/*.*", "!app/images/src/*.svg"], { encoding: false })
    .pipe(newer("dist/images"))
    .pipe(avif({ quality: 50 }))
    .pipe(dest("dist/images"));

  // Обрабатываем все изображения (включая SVG) с использованием imagemin
  return src("app/images/src/*.*", { encoding: false })
    .pipe(newer("dist/images"))
    .pipe(imagemin())
    .pipe(dest("dist/images"));
}

// Спрайт
function sprite() {
  return src("app/images/*.svg")
    .pipe(
      svgSprite({
        mode: {
          stack: {
            sprite: "../sprite.svg",
            example: true,
          },
        },
      })
    )
    .pipe(dest("app/images"));
}

// Обработка скриптов
// Dev
function scripts() {
  return src("app/js_src/main.js")
    .pipe(
      webpackStream(
        {
          mode: "development",
          output: {
            filename: "bundle.js",
          },
          module: {
            rules: [
              {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                  loader: "babel-loader",
                  options: {
                    presets: ["@babel/preset-env"],
                  },
                },
              },
            ],
          },
          plugins: [
            new webpack.ProvidePlugin({
              $: "jquery",
              jQuery: "jquery",
              "window.jQuery": "jquery",
            }), // Включение Jquery глобально
          ],
        },
        webpack
      )
    )
    .pipe(concat("main.min.js"))
    .pipe(uglify())
    .pipe(dest("app/js"))
    .pipe(browserSync.stream());
}

//Prod
function scriptsBuild() {
  return src("app/js_src/main.js")
    .pipe(
      webpackStream(
        {
          mode: "production",
          output: {
            filename: "bundle.js",
          },
          module: {
            rules: [
              {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                  loader: "babel-loader",
                  options: {
                    presets: ["@babel/preset-env"],
                  },
                },
              },
            ],
          },
          plugins: [
            new webpack.ProvidePlugin({
              $: "jquery",
              jQuery: "jquery",
              "window.jQuery": "jquery",
            }), // Включение Jquery глобально
          ],
        },
        webpack
      )
    )
    .pipe(concat("main.min.js"))
    .pipe(uglify())
    .pipe(rev())
    .pipe(dest("dist/js"))
    .pipe(rev.manifest())
    .pipe(dest("dist/js"))
    .pipe(browserSync.stream());
}

// Обновление ссылок в HTML
function updateReferencesJs() {
  const manifest = src("dist/js/rev-manifest.json");

  return src("dist/**/*.html")
    .pipe(revReplace({ manifest }))
    .pipe(dest("dist"));
}

// Обработка стилей
// Dev
function styles() {
  return src("app/scss/main.scss")
    .pipe(
      scss({
        implementation: sassCompiler,
        silenceDeprecations: [
          "legacy-js-api",
          "mixed-decls",
          "color-functions",
          "global-builtin",
          "import",
        ], // Игнорирование предупреждений
      }).on('error', function (err) {
        console.error('SCSS compile error:\n', err.message);
        this.emit('end'); // отслеживание ошибок
      })
    )
    .pipe(autoprefixer({ overrideBrowserslist: ["last 10 version"] }))
    .pipe(concat("style.min.css"))
    // .pipe(cleanCSS()) // можно убрать сжатие в режиме dev
    .pipe(replace("../webfonts/", "../fonts/")) // Замена путей для FontAwesome
    .pipe(dest("app/css"))
    .pipe(browserSync.stream());
}

// Prod
function stylesBuild() {
  return src("app/scss/main.scss")
    .pipe(
      scss({
        implementation: sassCompiler,
        silenceDeprecations: [
          "legacy-js-api",
          "mixed-decls",
          "color-functions",
          "global-builtin",
          "import",
        ], // Игнорирование предупреждений
      })
    )
    .pipe(autoprefixer({ overrideBrowserslist: ["last 10 version"] }))
    .pipe(concat("style.min.css"))
    .pipe(cleanCSS())
    .pipe(replace("../webfonts/", "../fonts/")) // Замена путей для FontAwesome
    .pipe(rev())
    .pipe(dest("dist/css"))
    .pipe(rev.manifest())
    .pipe(dest("dist/css"));
}

function updateReferencesCss() {
  const manifest = src("dist/css/rev-manifest.json");

  return src("dist/**/*.html")
    .pipe(revReplace({ manifest }))
    .pipe(dest("dist"));
}

// Слежение за файлами
function watching() {
  browserSync.init({
    server: {
      baseDir: "app/",
    },
  });
  watch(["app/scss/**/*.scss"], styles);
  watch(["app/images/src"], images);
  watch(["app/js_src/**/*.js"], scripts);
  watch(["app/components/*", "app/pages/*"], pages);
  watch(["app/fonts/src/*"], fonts);
  watch(["app/*.html"]).on("change", browserSync.reload);
}

// Очистка папки dist
function cleanDist() {
  return src("dist", { allowEmpty: true }).pipe(clean());
}

// Сбор
function building() {
  return src(
    [
      "!app/css/style.min.css",
      "!app/images/**/*.html",
      "!app/images/*.*",
      "!app/images/*.svg",
      "app/images/sprite.svg",
      "!app/fonts/*.*",
      "!app/js/main.min.js",
      "app/**/*.html",
      "!app/pages/**/*",
      "!app/components/**/*",
    ],
    { base: "app", allowEmpty: true }
  ).pipe(dest("dist"));
}

export {
  styles,
  images,
  copyFontAwesome,
  fonts,
  pages,
  building,
  sprite,
  scripts,
  watching,
};
export const build = series(
  cleanDist,
  copyFontAwesomeBuild,
  fontsBuild,
  scriptsBuild,
  stylesBuild,
  imagesBuild,
  building,
  updateReferencesJs,
  updateReferencesCss
);
export default parallel(
  styles,
  images,
  scripts,
  pages,
  copyFontAwesome,
  watching
);
