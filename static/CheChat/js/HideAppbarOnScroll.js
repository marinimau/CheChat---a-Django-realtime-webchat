var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    document.getElementById("appbar").style.top = "0";
      console.log(0);
  } else {
    document.getElementById("appbar").style.top = "-60px";
      console.log(1);
  }
  prevScrollpos = currentScrollPos;
}
