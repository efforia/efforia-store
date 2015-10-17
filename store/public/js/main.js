var navbar = 84; /* Navbar actual size */
var minheight = 450; /* Minimum actual height */

function changeLocale(locale) {
  $('#language').val(locale);
  $('#locale').submit();
}

function submenuOnTop() {
  // Put submenu on top after scrolling navbar; returns when scrolls back
  var submenu = $('.subnavbar');
  $(document).scroll(function(event){
    var scrollsTop = $(this).scrollTop();
    if(scrollsTop >= navbar) submenu.addClass('navbar-fixed-top').css('position','fixed').children().css('top',0);
    else submenu.removeClass('navbar-fixed-top').css('position','static').children().css('top',84);
  });
}

function jumbotronOffset() {
  // Jumbotron offsetting on home page based on viewport and jumbotron min-height
  var viewport = $(window).height(); /* Viewport height */
  if(viewport >= minheight) $('.jumbotron').css({'min-height': viewport - navbar});
}

function minimumHeight() {
  // Footer offsetting for fixed width on Bootstrap
  var height = $("body").height();
  var offset = height - viewport;
  if(offset > 0) $('footer').css({'margin-bottom':'0px'});
  else $('footer').css({
    'bottom':'0px',
    'position':'absolute',
    'width':'100%'
  });
}

function main() {
  submenuOnTop();
  jumbotronOffset();
}

$(window).load(main);
