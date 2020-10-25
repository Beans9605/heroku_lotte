var preBought = document.getElementById('option1');
var all_set = document.getElementById('option2');
var recomend_pd = document.getElementById('option3');

var slide1 = document.getElementById('click1');
var slide2 = document.getElementById('click2');
var slide3 = document.getElementById('click3');

preBought.addEventListener('click', function(){
  slide1.style.zIndex = '1';
  slide2.style.zIndex = '0';
  slide3.style.zIndex = '0';

});

all_set.addEventListener('click', function(){
  slide1.style.zIndex = '0';
  slide2.style.zIndex = '1';
  slide3.style.zIndex = '0';

});

recomend_pd.addEventListener('click', function(){
  slide1.style.zIndex = '0';
  slide2.style.zIndex = '0';
  slide3.style.zIndex = '1';

});
