//Global variable and functions
const sleep = (milliseconds) => {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
};

var countMarker = null;
var map = null;
let updateMapIcone = () => {
  if (countMarker.length == 2) {
    var takeoff = L.icon({
      iconUrl: baseUrl + "/static/dmc/img/takeoff.png",
      iconSize: [70, 100],
      iconAnchor: [35, 95],
      // shadowAnchor: [4, 62],
      popupAnchor: [-3, -76],
    });
    countMarker[0].setIcon(takeoff);

    var landed = L.icon({
      iconUrl: baseUrl + "/static/dmc/img/landed.png",
      iconSize: [70, 100],
      iconAnchor: [35, 95],
      // shadowAnchor: [4, 62],
      popupAnchor: [-3, -76],
    });

    countMarker[1].setIcon(landed);

// fit the map extent
map.fitBounds(L.featureGroup([countMarker[0],countMarker[1]]).getBounds());

sleep(1000).then(() => {
map.zoomOut(1);
});
  }
};



// before page load
window.onload = function (e) {
  // fix to the base template
  $.backstretch("destroy", 0);
};

document.addEventListener("DOMContentLoaded", function () {
  // fix to the base template
  document.querySelectorAll(".tm-bg").forEach((el) => el.remove());
  document.querySelectorAll(".tm-bg-controls-wrapper")[0].remove();


  // initialize the datepiker calader
  $.fn.datepicker.defaults.format = 'yyyy-mm-dd';

  baseUrl = window.location.origin;

  $(window).on("map:init", function (e) {
    //get the map refrence
    var detail = e.originalEvent ? e.originalEvent.detail : e.detail;
    map = detail.map;

    // add location based on the serch
    map.on("locationfound", onLocationFound);
    var searchControl = L.esri.Geocoding.geosearch({
      position: "topright",
      useMapBounds: false,
    }).addTo(map);

    // map locate control setups
    map.locate({ setView: true, maxZoom: 16 });
    L.control
      .locate({ position: "topright", icon: "fa fa-location-arrow" })
      .addTo(map);

    // serch location on map
    function onLocationFound(e) {
      if (map.getZoom() > 17) {
        map.setZoom(17);
      }
    }

    // create a fullscreen button and add it to the map
    L.control
      .fullscreen({
        position: "topleft", // change the position of the button can be topleft, topright, bottomright or bottomleft, default topleft
        title: "Show me the fullscreen !", // change the title of the button, default Full Screen
        titleCancel: "Exit fullscreen mode", // change the title of the button when fullscreen is on, default Exit Full Screen
        content: null, // change the content of the button, can be HTML, default null
        forceSeparateButton: false, // force separate button to detach from zoom buttons, default false
        forcePseudoFullscreen: false, // force use of pseudo full screen even if full screen API is available, default false
        fullscreenElement: false, // Dom element to render in full screen, false by default, fallback to map._container
      })
      .addTo(map);

    //update the zoom to extent icone
    document.getElementsByClassName(
      "leaflet-control-zoom-out leaflet-bar-part"
    )[0].style = "";
    document.getElementsByClassName(
      "leaflet-control-zoom-out leaflet-bar-part"
    )[0].innerHTML = '<i class="fa fa-globe-americas fa-xs"></i>';

    var results = L.layerGroup().addTo(map);

    searchControl.on("results", function (data) {
      results.clearLayers();
      for (var i = data.results.length - 1; i >= 0; i--) {
        results.addLayer(
          L.circleMarker(data.results[i].latlng, {
            color: "#FF0000",
            radius: 8,
            className: "blinking",
            fill: true,
          })
        );
      }
    });

    // restrict the number of points
    map.on("draw:created", function (e) {
      updatecountMarker(map._layers);

      if (countMarker.length > 2) {
        document.querySelector('a[title="Cancel drawing"]').click();
        $.confirm({
          title:
            '<i class="fa fa-exclamation-triangle text-danger"> Not Allowed</i> ',
          content:
            '<span class="text-danger" >Map will record only two points one for Take-off and second point for landing co-ordinates <span/>',
          typeAnimated: true,
          type: "orange",
          buttons: {
            info: {
              btnClass: "btn-default",
              text: "Close",
            },
          },
        });
      }

      sleep(1000).then(() => {
        updatecountMarker(map._layers);
      });
    });

    map.on("draw:deleted", function (e) {
      updatecountMarker(map._layers);
    });
  });

  /*
// drop down to checkbox dropdown
$('#id_wind_direction').multiselect(
{
 buttonWidth: '100%',
 enableFiltering: true

});
/
// dropdown to checkbox dropdown
$('#id_sensor_info').multiselect(
{
 buttonWidth: '50%',
 enableFiltering: true,

});*/

  //#######################################

  var btnSave = $(
    '<button id="btn_saveData" class= "btn btn-info btn_saveData_extraClass"  type="submit" value="Save"></button>'
  )
    .text("Save")
    .on("click", function (e) {
      // e.preventDefault();

    });

  var btnList = $(
    '<button class= "btn btn-info" value="Input"  type="button"><i class="fas fa-solid  fa-list-ol"></i></button>'
  ).on("click", function (e) {
    e.preventDefault();
    window.location.href = "/dmc/list";
  });

  $("#smartwizard").smartWizard({
    selected: 0, // Initial selected step, 0 = first step
    theme: "dots", // theme for the wizard, related css need to include for other than default theme
    justified: true, // Nav menu justification. true/false
    darkMode: false, // Enable/disable Dark Mode if the theme supports. true/false
    autoAdjustHeight: true, // Automatically adjust content height
    cycleSteps: false, // Allows to cycle the navigation of steps
    backButtonSupport: true, // Enable the back button support
    enableURLhash: true, // Enable selection of the step based on url hash
    transition: {
      animation: "fade", // Effect on navigation, none/fade/slide-horizontal/slide-vertical/slide-swing
      speed: "400", // Transion animation speed
      easing: "", // Transition animation easing. Not supported without a jQuery easing plugin
    },
    toolbarSettings: {
      toolbarPosition: "top", // none, top, bottom, both
      toolbarButtonPosition: "right", // left, right, center
      showNextButton: true, // show/hide a Next button
      showPreviousButton: true, // show/hide a Previous button
      toolbarExtraButtons: [btnSave, btnList], // Extra buttons to show on toolbar, array of jQuery input/buttons elements
    },
    anchorSettings: {
      anchorClickable: true, // Enable/Disable anchor navigation
      enableAllAnchors: false, // Activates all anchors clickable all times
      markDoneStep: true, // Add done state on navigation
      markAllPreviousStepsAsDone: true, // When a step selected by url hash, all previous steps are marked done
      removeDoneStepOnNavigateBack: false, // While navigate back done step after active step will be cleared
      enableAnchorOnDoneStep: true, // Enable/Disable the done steps navigation
    },
    keyboardSettings: {
      keyNavigation: true, // Enable/Disable keyboard navigation(left and right keys are used if enabled)
      keyLeft: [37], // Left key code
      keyRight: [39], // Right key code
    },
    lang: {
      // Language variables for button
      next: "Next",
      previous: "Previous",
    },
    disabledSteps: [], // Array Steps disabled
    errorSteps: [], // Highlight step with errors
    hiddenSteps: [], // Hidden steps
  });

  //#################################

  //### add click event to checkbox

  Array.from(document.getElementById('div_id_dron_info').querySelectorAll(".form-check")).forEach(function (
    element
  ) {
    var orgtag = element.innerHTML;
    var btnTag =
      "<button type='button' class='btn btn-link p-0 m-0 pr-5 mr-5 float-right' onclick='getDeviceInfo()'> <i class='fa fa-info-circle text-info m-0 p-0'></i></button>";
    element.innerHTML = orgtag + btnTag;
  });

    Array.from(document.getElementById('div_id_sensor_info').querySelectorAll(".form-check")).forEach(function (
    element
  ) {
    var orgtag = element.innerHTML;
    var btnTag =
      "<button type='button' class='btn btn-link float-right p-0 m-0 pt-1' onclick='getDeviceInfo()'> <i class='fa fa-info-circle text-info m-0 p-0 float-right'></i></button> \
      <button type='button' class='btn btn-link float-right p-0 m-0 pr-2 ' onclick='updateDeviceInfo()'> <i class='fa fa-edit text-info m-0 p-0'></i></button>";
    element.innerHTML = orgtag + btnTag;
  });


});

// hide data picker
/*$('.datepicker').on('changeDate', function(ev){
    $(this).datepicker('hide');
});*/



// datatime format initialize

function getDeviceInfo() {
  $("#tbody_drone").empty();
  if (
    this.event.currentTarget.parentElement.getElementsByTagName("input")[0]
      .name == "dron_info"
  ) {



    $.getJSON(
      "/dmc/drone/" +
        this.event.currentTarget.parentElement.getElementsByTagName("label")[0]
          .innerText.split('/').pop(),
      function () {}
    )
      .done(function (data) {
        document.getElementById("staticBackdropLabelD").innerText =
          "Drone Details";


  $("#tbody_drone").append(
          "<tr><td><b>1</b></td><td>Manufacturer</td><td><b>" +
            (data.manufacturer == null ? "-" : data.manufacturer) +
            "</b></td></tr>"
        );


        $("#tbody_drone").append(
          "<tr><td><b>2</b></td><td>Make</td><td><b>" +
            (data.make == null ? "-" : data.make) +
            "</b></td></tr>"
        );

        $("#tbody_drone").append(
          "<tr><td><b>3</b></td><td>ID</td><td><b>" +
            (data.drone_srnr == null ? "-" : data.drone_srnr) +
            "</b></td></tr>"
        );
        $("#tbody_drone").append(
          "<tr><td><b>4</b></td><td>Model</td><td><b>" +
            (data.model == null ? "-" : data.model) +
            "</b></td></tr>"
        );
        $("#tbody_drone").append(
          "<tr><td><b>5</b></td><td>Type</td><td><b>" +
            (data.type == null ? "-" : data.type) +
            "</b></td></tr>"
        );
        $("#tbody_drone").append(
          "<tr><td><b>6</b></td><td>Year</td><td><b>" +
            (data.year == null ? "-" : data.year) +
            "</b></td></tr>"
        );



        $("#dronSensoreInfo").modal("show");
      })
      .fail(function () {
        console.log("error");
      });
  }

  if (
    this.event.currentTarget.parentElement.getElementsByTagName("input")[0]
      .name == "sensor_info"
  ) {
    $.getJSON(
      "/dmc/sensor/" +
        this.event.currentTarget.parentElement.getElementsByTagName("label")[0]
          .innerText,
      function () {}
    )
      .done(function (data) {
        document.getElementById("staticBackdropLabelD").innerText =
          "Senson Details";




        $("#tbody_drone").append(
          "<tr><td><b>1</b></td><td>Model</td><td><b>" +
            (data.model == null ? "-" : data.model) +
            "</b></td></tr>"
        );
        $("#tbody_drone").append(
          "<tr><td><b>2</b></td><td>Make</td><td><b>" +
            (data.make == null ? "-" : data.make) +
            "</b></td></tr>"
        );
        $("#tbody_drone").append(
          "<tr><td><b>3</b></td><td>Resolution</td><td><b>" +
            (data.resolution == null ? "-" : data.resolution) +
            "</b></td></tr>"
        );
        $("#tbody_drone").append(
          "<tr><td><b>4</b></td><td>Sensor Size</td><td><b>" +
            (data.sensor_size == null ? "-" : data.sensor_size) +
            "</b></td></tr>"
        );
        $("#tbody_drone").append(
          "<tr><td><b>5</b></td><td>Type</td><td><b>" +
            (data.type == null ? "-" : data.type) +
            "</b></td></tr>"
        );

        $("#tbody_drone").append(
          "<tr><td><b>6</b></td><td>Band Wavelength Intervals</td><td><b>" +
            (data.band_wavelength_intervals == null
              ? "-"
              : data.band_wavelength_intervals) +
            "</b></td></tr>"
        );

               $("#tbody_drone").append(
          "<tr><td><b>7</b></td><td>Dates of last calibration</td><td><b>" +
            (data.dates_last_calibration == null
              ? "-"
              : data.dates_last_calibration) +
            "</b></td></tr>"
        );


               $("#tbody_drone").append(
          "<tr><td><b>8</b></td><td>Dates of last maintenance</td><td><b>" +
            (data.dates_last_maintenance == null
              ? "-"
              : data.dates_last_maintenance) +
            "</b></td></tr>"
        );

        $("#dronSensoreInfo").modal("show");
      })
      .fail(function () {
        console.log("error");
      });
  }
}

var sensorModelID=null;
function updateDeviceInfo()
{

 $("#updateSensorModelForm").modal("show");
var sensorModelName =  this.event.currentTarget.parentElement.getElementsByTagName("label")[0].innerText;

  $.getJSON(
      "/dmc/sensor/" + sensorModelName,
      function () {}
    )
      .done(function (data) {
            document.getElementById('inputCalibrationUpdate').value = (data.dates_last_calibration == "" ? "": data.dates_last_calibration);
            document.getElementById('inputMaintenanceUpdate').value = (data.dates_last_maintenance == "" ? "": data.dates_last_maintenance);
            sensorModelID = data.id;
      })
      .fail(function () {
        console.log("error");
      });



}


// funxtion to update the sensor data
function CloseUpdateSensorModelWindow(){


 var data = {

        dates_last_calibration: document.getElementById('inputCalibrationUpdate').value,
        dates_last_maintenance: document.getElementById('inputMaintenanceUpdate').value,
      };



     // const csrftoken = getCookie("csrftoken"); // HERE: get the token
      $.ajax({
        type: "PATCH",
        data: data,
        headers: { "X-CSRFToken": document.getElementsByName('csrfmiddlewaretoken')[0].value },
        url: "/dmcapi/addsensor/"+ sensorModelID + "/",
        success: function (res) {

                 $("#updateSensorModelForm").modal("hide");

        },
        error: function (res) {
          var errorMessage = res.status + ": " + res.statusText;
          console.error("Error Posting: ", errorMessage);
        },
      });




}













function addDeviceInfo() {
  if (this.event.currentTarget.name == "drone") {
    $("#addDroneForm")[0].reset();
    $("#addNewDrone").modal("show");
  }
  if (this.event.currentTarget.name == "sensor") {
    $("#addSensorForm")[0].reset();
    $("#addNewSensor").modal("show");
  }
}

function CloseDroneSensorModelWindow() {
  if (this.event.target.name == "drone") {
    if (document.getElementById("addDroneForm").checkValidity()) {
      $("#addNewDrone").modal("hide");

      var data = {
        drone_srnr: document.getElementById("inputID").value,
        make: document.getElementById("inputMake").value,
        model: document.getElementById("inputModel").value,
        type: document.getElementById("inputType").value,
        year: document.getElementById("inputYear").value,
        manufacturer: document.getElementById("inputmanufacturer").value,


      };



     // const csrftoken = getCookie("csrftoken"); // HERE: get the token
     //var  csrftoken= document.getElementsByName('csrfmiddlewaretoken')[0].value ;
      $.ajax({
        type: "POST",
        data: data,
        headers: { "X-CSRFToken": document.getElementsByName('csrfmiddlewaretoken')[0].value },
        url: "/dmcapi/adddrone/",
        success: function (res) {

                updateSensorDronePageUpdate();

        },
        error: function (res) {
          var errorMessage = res.status + ": " + res.statusText;
          console.error("Error Posting: ", errorMessage);
        },
      });
    } else {
     if(document.getElementById("inputmanufacturer").value.length < 1)
      document.getElementById("droneManufacturer").classList.add("was-validated");

       if(document.getElementById("inputMake").value.length <  1)
      document.getElementById("droneMake").classList.add("was-validated");

         if(document.getElementById("inputID").value.length <  1)
          document.getElementById("droneID").classList.add("was-validated");

         if(document.getElementById("inputModel").value.length <  1)
         document.getElementById("droneModel").classList.add("was-validated");

    }
  }

  if (this.event.target.name == "sensor") {
    if (document.getElementById("addSensorForm").checkValidity()) {
      $("#addNewSensor").modal("hide");

      var data = {
        make: document.getElementById("inputMakeS").value,
        model: document.getElementById("inputModelS").value,
        type: document.getElementById("inputTypeS").value,
        sensor_size: document.getElementById("inputSensorSize").value,
        resolution: document.getElementById("InputResolutionID").value,
        band_wavelength_intervals: document.getElementById("inputWave").value,
        dates_last_calibration: document.getElementById("inputCalibration").value,
        dates_last_maintenance: document.getElementById("inputMaintenance").value,
      };



     // const csrftoken = getCookie("csrftoken"); // HERE: get the token
      $.ajax({
        type: "POST",
        data: data,
        //csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value , // Set the headers in the request
        headers: { "X-CSRFToken": document.getElementsByName('csrfmiddlewaretoken')[0].value },
        url: "/dmcapi/addsensor/",
        success: function (res) {

                updateSensorDronePageUpdate();



        },
        error: function (res) {
          var errorMessage = res.status + ": " + res.statusText;
          console.error("Error Posting: ", errorMessage);
        },
      });
    } else {
      document.getElementById("SensorModel").classList.add("was-validated");
    }
  }
}




function updateSensorDronePageUpdate(){

    var uploadForm = document.getElementById("containerForm");
    var formData = new FormData(uploadForm);

   $.ajax({
      type: "POST",
      url: uploadForm.action,
      enctype: "multipart/form-data",
      data: formData,

      success: function (response) {
        console.log(response);


    if ( response.entryType == "update"  ) {
          location.reload();
          window.location.href = "/dmc/" + response.pk + "/#step-2";
          location.reload();
        }

        if ( response.entryType == "new" ) {
          window.location.href = "/dmc/" + response.pk + "/#step-2";
        }

      },
      error: function (err) {
        console.log("error---" + err);
        alert(err);
      },
      cache: false,
      contentType: false,
      processData: false,
    });


}


/*function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}*/

sleep(2000).then(() => {
  //console.log(map._layers);
  updatecountMarker(map._layers);
});

function updatecountMarker(obj) {
  countMarker = [];
  Object.entries(obj).map((item) => {
    if (
      item[1] instanceof L.Marker &&
      item[1]._icon.className ==
        "leaflet-marker-icon leaflet-zoom-animated leaflet-interactive"
    ) {
      countMarker.push(item[1]);
    }
  });
  updateMapIcone();
}
// make a defult call
//submitMainForm();
//function submitMainForm() {
  $("#containerForm").submit(function (e) {
    e.preventDefault();
    $form = $(this);

    var formData = new FormData(this);
    var uploadForm = document.getElementById("containerForm");

    var progress_bar = document.getElementById("progress_dataUpload");

    var input_file_mosaiced_image =
      document.getElementById("id_mosaiced_image").files[0];
    var input_file_row_image = document.getElementById("id_row_image").files[0];
    var input_file_ground_control_point = document.getElementById(
      "id_ground_control_point"
    ).files[0];
    var input_file_ground_truth_point = document.getElementById(
      "id_ground_truth_point"
    ).files[0];
    var input_file_dronePath = document.getElementById("id_dronePath").files[0];

    if (
      input_file_mosaiced_image != null ||
      input_file_row_image != null ||
      input_file_ground_control_point != null ||
      input_file_ground_truth_point != null ||
      input_file_dronePath != null
    ) {
      // console.log(media_data);
      progress_bar.classList.remove("d-none");
    }

    return $.ajax({
      type: "POST",
      url: uploadForm.action,
      enctype: "multipart/form-data",
      data: formData,

      // dataType: 'json',

      beforeSend: function () {
        // $("#smartwizard").smartWizard("loader", "show");
      },
      xhr: function () {
        const xhr = new window.XMLHttpRequest();
        xhr.upload.addEventListener("progress", (e) => {
          if (e.lengthComputable) {
            const percentProgress = (e.loaded / e.total) * 100;
            console.log(percentProgress);
            progress_bar.innerHTML = `<div class="progress-bar progress-bar-striped bg-success progress-bar-animated text-white"
                    role="progressbar" style="width: ${percentProgress}%" aria-valuenow="${percentProgress}" aria-valuemin="0"
                    aria-valuemax="100"> <b> ${Math.round(
                      percentProgress
                    )} %</b>  </div>`;
          }
        });
        console.log("xhr---" + xhr);
        return xhr;
      },
      success: function (response) {
        console.log(response);
        progress_bar.classList.add("d-none");
        //  $("#smartwizard").smartWizard("loader", "hide");
        // reload to see if any panding form message
        // fix for new drone or sensor entry && $('#smartwizard').smartWizard("getStepIndex") != 1



        if (
          response.entryType == "update"  &&
          $("#smartwizard").smartWizard("getStepIndex") != 1
        ) {
          location.reload();
          window.location.href = "/dmc/" + response.pk + "/#step-5";
          location.reload();
        }

        if (
          response.entryType == "new"  &&
          $("#smartwizard").smartWizard("getStepIndex") != 1
        ) {
          window.location.href = "/dmc/" + response.pk + "/#step-5";
        }else

        if ($("#smartwizard").smartWizard("getStepIndex") == 1) {
          location.reload();
        }



      },
      error: function (err) {
        console.log("error---" + err);
        alert(err);
      },
      cache: false,
      contentType: false,
      processData: false,
    });
  });
//}

$("#smartwizard").on(
  "showStep",
  function (e, anchorObject, currentStepIndex, stepDirection) {
    //
    if (currentStepIndex == 3) {
      Array.from(
        document.getElementsByClassName("btn_saveData_extraClass")
      ).forEach((x) => {
        x.disabled = false;
      });
      Array.from(document.getElementsByClassName("sw-btn-next")).forEach(
        (x) => {
          x.disabled = true;
        }
      );
    } else {
      Array.from(
        document.getElementsByClassName("btn_saveData_extraClass")
      ).forEach((x) => {
        x.disabled = true;
      });
      Array.from(document.getElementsByClassName("sw-btn-next")).forEach(
        (x) => {
          x.disabled = false;
        }
      );
    }

    if (currentStepIndex == 0) {
      // validate the map
      map.invalidateSize();
    }
  }
);
