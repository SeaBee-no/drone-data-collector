//doc ready
document.addEventListener("DOMContentLoaded", function () {

  // fix to the base template
  document.querySelectorAll(".tm-bg").forEach((el) => el.remove());
  document.querySelectorAll(".tm-bg-controls-wrapper")[0].remove();


});

//});

// before page load
window.onload = function (e) {
  // fix to the base template
  $.backstretch("destroy", 0);
};


// Delete DOI
dmcdelBypk = (obj) => {


        // alert fetch data
        $.confirm({
          title:
            '<i class="fa fa-exclamation-triangle text-danger">Warning!</i> ',
          content:
            '<span class="text-danger"><b>Delete this item?</b><span/>',
          typeAnimated: true,
          type: "red",
          buttons: {

         warning: {
           btnClass: 'btn-danger',
           text: "Delete",
           action: function(){

            window.location.href = "/dmc/"+obj+"/del";

            },
            },
          info: {
           btnClass: 'btn-default',
           text: "Cancel",
            },


          },
        });




};