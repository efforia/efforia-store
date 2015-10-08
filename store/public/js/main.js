function changeLocale(locale) {
  $('#language').val(locale);
  $('#locale').submit();
}

$(document).ready(function(){
  var viewport = $(window).height();

  // Footer offsetting for fixed width on Bootstrap
  var height = $(document).height();
  var offset = height - viewport;
  if(offset > 0) $('footer').css({'margin-bottom':'0px'});
  else $('footer').css({
    'bottom':'0px',
    'position':'absolute',
    'width':'100%'
  });

  // Jumbotron offsetting on home page based on viewport and jumbotron min-height
  if(viewport >= 720) $('.jumbotron').css({'min-height': $(window).height() - 84});
});
