var i = 0;

//Get the next image and submit all of the oocytes from the last image
function nextImg() {
  i++;
  for(let j = 0; j < clicked.length; j++){
    $.ajax({
          url: 'ajax/up_oocyte/',
          data: {
            'id': clicked[j][2]
          }
    });
    $('#block' + Math.floor(clicked[j][0])).remove();
  }
  clicked = [];
  if(i<8)
    hide_inactive_images();
}

//Hide all of the inactive divs and only show current one
function hide_inactive_images(){
  for(let j = 0; j < 8; j++){
    if(j != i)
      $("#image" + j).hide();
    else
      $("#image" + j).show();
  }
}

//Hide the divs to start off
$(document).ready(function() {
  hide_inactive_images();
});

var clicked = [];
$(document).ready(function() {
  //Attach a handler to each of the images for when they become visible
  for(let k = 0; k< 8; k++){
    $("#binarized"+k).on("click", function(event) {
        var offsetL = this.offsetLeft;
        var offsetT = this.offsetTop;
        var x = event.pageX - offsetL;
        var y = event.pageY - offsetT;
        var photo = $("#img" + k).val();
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
            var pt = [data.xcenter, data.ycenter, data.id];
            var undone = -1;
            //Only add to clicked if it hasn't been
            //selected before
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
                  $('<div id = "block' + Math.floor(data.xcenter) + '">'+clicked.length+'</div>').css({
                      position: 'absolute',
                      top: offsetT+ pt[1] - 10 + 'px',
                      left: offsetL+ pt[0] - 10 + 'px',
                      width: '20px',
                      height: '20px',
                      paddingLeft: '6px',
                      color: '#FFFFFF',
                      background: '#000000',

                  })              
                );
              }  
              else{
                console.log(clicked.length);
                $('#block' + Math.floor(data.xcenter)).text(clicked.length);
                $('#block' + Math.floor(data.xcenter)).toggle();

              }
            }
            //If already clicked, undo and remove from array
            else{
              var div = '#block' + Math.floor(data.xcenter);
              clicked.splice(undone, 1);
              $(div).toggle();
            }
          }
        });
    });
  }
});



