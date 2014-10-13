/**
 * This example:
 *  Shows how to plug in the details of your server.
 *  Watches & injects CSS files
 */
var gulp         = require('gulp');
var browserSync  = require('browser-sync');
var reload       = browserSync.reload;
var sass         = require('gulp-sass');
var bourbon      = require('node-bourbon');
var autoprefixer = require('gulp-autoprefixer');

// Browser-sync task, only cares about compiled CSS
gulp.task('browser-sync', function() {
  browserSync({
    files: 'public/css/*.css',
    proxy: {
      port: 5000,
    },
  });
});

// Copy static assets
gulp.task('bs-reload', function () {
  gulp.src('assets/*.html')
    .pipe(gulp.dest('public/'))
    .pipe(reload({stream: true}))
});

// Sass task, will run when any SCSS files change.
gulp.task('sass', function () {
  gulp.src('assets/scss/styles.scss')
    .pipe(sass({
      includePaths: ['scss', bourbon.includePaths],
      errLogToConsole: true
    }))
    .pipe(autoprefixer())
    .pipe(gulp.dest('public/css/'))
    .pipe(reload({stream: true}));
});

// Default task to be run with `gulp`
gulp.task('default', ['sass', 'browser-sync'], function () {
  gulp.watch('assets/scss/*.scss', ['sass']);
  gulp.watch('assets/*.html', ['bs-reload']);
});