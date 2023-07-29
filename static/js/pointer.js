$(function(){
  var app=$("#app");
  $(document).on("mousemove",function(e){
    var x=e.clientX;
    var y=e.clientY;
    app.css({
      "opacity":"1",
      "top":y+"px",
      "left":x+"px"
    });
  });

  $("a").on({
    "mouseenter": function() {
      app.addClass("active");
    },
    "mouseleave": function() {
      app.removeClass("active");
    }
  });
});