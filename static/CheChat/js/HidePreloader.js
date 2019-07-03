window.onload = function() {
  hidePreloader();
};

function hidePreloader(){
    setTimeout(function(){
        document.getElementById("preloader").style.display="none";
    } , 200);

}