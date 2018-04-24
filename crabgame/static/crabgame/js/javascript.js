var i = 0;
function nextImg() {
  i++;
  console.log("i");
  if (i == 9) {
    document.write("Game Over");
    return;
  }
  else {
    var photo = photos[i];
    document.getElementById("originalNxt").setAttribute("src", "media/"{{photo.crab.sample_num}}"/untitled"{{photo.get_img_num }}"_resize.png");
    document.getElementById("binarizedNxt").setAttribute("src", "media/"{{photo.crab.sample_num }}"/untitled"{{ photo.get_img_num }}"_label.png")
  }
};

var clicked = [];
$(document).ready(function() {
    $("#binarized").on("click", function(event) {
        var offsetL = this.offsetLeft;
        var offsetT = this.offsetTop;
        var x = event.pageX - offsetL;
        var y = event.pageY - offsetT;
        var photo = $("#img0").val();
        $.ajax({
          url: 'ajax/find_oocyte/',
          dataType: "json",
          data: {
            'xclick': x,
            'yclick': y,
            'photoid': photo
          },
          //On click, place a dot at center
          //to provide feedback
          success: function(data){
            var pt = [data.xcenter, data.ycenter];
            var undone = -1;
            //Only add to clicked if it hasn't been
            //selected before
            /*clicked.forEach(function(element){
              console.log(element)
              if(element[0] == pt[0] && element[1] == pt[1])
                undone = true;
            })*/
            for(let i = 0; i<clicked.length; i++){
              element = clicked[i];
              if(element[0] == pt[0] && element[1] == pt[1])
                undone = i;
            }
            //If not clicked before, add to array and draw circle
            if(undone < 0){
              clicked.push(pt);
              if($('#block' + Math.floor(data.xcenter)).length == 0){
                $("body").append(            
                  $('<div id = "block' + Math.floor(data.xcenter) + '"></div>').css({
                      position: 'absolute',
                      top: offsetT+ pt[1] - 10 + 'px',
                      left: offsetL+ pt[0] - 10 + 'px',
                      width: '20px',
                      height: '20px',
                      background: '#000000'
                  })              
                );
              }  
              else{
                $('#block' + Math.floor(data.xcenter)).toggle();
              }
            }
            //If already clicked, undo and remove from array
            else{
              var div = '#block' + Math.floor(data.xcenter);
              clicked.splice(undone, 1);
              console.log(clicked);
              console.log("divs: " + $(div).length);
              $(div).toggle();
            }
            console.log(clicked);
            console.log(undone);
          }
        });
    });


    $("#next").click(function (){
      $("#firstImg").hide();
      $("#nextImg").show();
      nextImg();
    });
});



