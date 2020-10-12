$(document).ready(function(){
    $('step').hover(function() {
        $(this).css("cursor", "pointer");
        $(this).toggle({
          effect: "scale",
          percent: "90%"
        },200);
    }, function() {
         $(this).toggle({
           effect: "scale",
           percent: "80%"
         },200);

    });
});