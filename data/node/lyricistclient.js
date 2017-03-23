var secrets = require('./secrets.js');
var lyricist = require('lyricist')(secrets.geniustoken);

lyricist.song(714198, function (err, song) {
  console.log(song.lyrics);
});

