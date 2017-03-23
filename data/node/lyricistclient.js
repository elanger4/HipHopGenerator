var secrets = require('./secrets.js');
var lyricist = require('lyricist')(secrets.geniustoken);

//lyricist.song(714198, function (err, song) {
//  console.log(song);
//});

//lyricist.artist({search: "Coldplay"}, function(err, artist) {
//  if (err)
//    console.log(err);
//  console.log(artist);
//});

//lyricist.song({ search: 'Kanye West Famous' }, function (err, song) {
//  console.log('%s - %s', song.primary_artist.name, song.title);
//});

lyricist.artist(2, { get_songs: true },function(err, artist) {
  console.log(artist);
});



//lyricist.song({ search: 'Kanye West Famous' }, function (err, song) {
//lyricist.song({ search: 'Lil Wayne Not a human being' }, function (err, song) {
//  console.log(song);
//});

