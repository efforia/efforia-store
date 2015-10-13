function changeLocale(locale) {
  $('#language').val(locale);
  $('#locale').submit();
}

$(window).load(function(){

  // Footer offsetting for fixed width on Bootstrap
  /* var height = $("body").height();
  console.log(height);
  console.log(viewport);
  var offset = height - viewport;
  if(offset > 0) $('footer').css({'margin-bottom':'0px'});
  else $('footer').css({
    'bottom':'0px',
    'position':'absolute',
    'width':'100%'
  }); */

  // Jumbotron offsetting on home page based on viewport and jumbotron min-height
  var navbar = 84; /* Navbar actual size */
  var minheight = 450; /* Minimum actual height */
  var viewport = $(window).height(); /* Viewport height */
  if(viewport >= minheight) $('.jumbotron').css({'min-height': viewport - navbar});
});
