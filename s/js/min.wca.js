$(document).ready(function(){if(document.cookie.match("disclaimer")!=null){$("#disclaimer").hide()}$("#ackbutton").click(function(){$.ajax({type:"POST",url:"/setcookie",success:function(){$("#disclaimer").hide()}})})});$(document).ready(function(){var a=location.href.split(/\//)[3].split(/#/)[0];if(a){if(a.indexOf(".")==-1){a+="/"}}else{a="index.html"}$("header ul.nav").find('a[href$="'+a+'"]').parents("li").addClass("active")});$(document).ready(function(){var g=$(window),a=$(".subnav"),e=$(".mainContentWrap"),d=$(".brand"),c=$(".subnav").length&&$(".subnav").offset().top-45,f=0;b();a.on("click",function(){if(!f){setTimeout(function(){g.scrollTop(g.scrollTop()-47)},10)}});g.on("scroll",b);function b(){if($(this).width()<767){}else{var h,j=g.scrollTop();if(j>=c&&!f){f=1;a.addClass("subnav-fixed");e.addClass("subnav-main-spacer");d.addClass("scroll-logo");$("img",d).hide()}else{if(j<=c&&f){f=0;a.removeClass("subnav-fixed");e.removeClass("subnav-main-spacer");d.removeClass("scroll-logo");$("img",d).show()}}}}});