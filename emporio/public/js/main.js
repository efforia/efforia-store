var navbar = 84; /* Navbar actual size */
var minheight = 450; /* Minimum actual height */

function redirect(addr){
  window.location = addr;
}

function changeLocale(locale) {
  $('#language').val(locale);
  $('#locale').submit();
}

function submenuOnBottom() {
  // Put submenu on bottom after scrolling navbar; returns when scrolls back
  var submenu = $('.subnavbar');
  var viewport = $(window).height();
  $(document).scroll(function(event){
    var scrollsTop = $(this).scrollTop();
    if(scrollsTop >= viewport - navbar) submenu.addClass('navbar-fixed-top').css('position','fixed').children().css('top',0);
    else submenu.removeClass('navbar-fixed-top').css('position','static').children().css('top',viewport-63);
  });
}

function submenuOnTop() {
  // Put submenu on top after scrolling navbar; returns when scrolls back
  var submenu = $('.subnavbar-top');
  var viewport = $(window).height();
  $(document).scroll(function(event){
    var scrollsTop = $(this).scrollTop();
    if(scrollsTop >= navbar) submenu.addClass('navbar-fixed-top').css('position','fixed').children().css('top',0);
    else submenu.removeClass('navbar-fixed-top').css('position','static').children().css('top',84);
  });
}

function jumbotronOffset() {
  // Jumbotron offsetting on home page based on viewport and jumbotron min-height
  var viewport = $(window).height(); /* Viewport height */
  if(viewport >= minheight){
    $('.jumbotron').css({'min-height':viewport-navbar});
    $('.submenu').css({'top':viewport-63});
  }
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
  submenuOnBottom();
  submenuOnTop();
  jumbotronOffset();
}

$(window).load(main);
