//Global variable and functions
const sleep = (milliseconds) => {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
};

// before page load
window.onload = function (e) {
  // fix to the base template
  $.backstretch("destroy", 0);
};

//get the base url of the current page
const baseUrl = window.location.origin;

//drone logo
const droneIcone = L.icon({
  iconUrl: baseUrl + "/static/dmc/img/landed.png",
  iconSize: [50, 70],
  iconAnchor: [25, 65],
  // shadowAnchor: [4, 62],
  popupAnchor: [-3, -76],
});

// initialize the map
let map_projArea = null;
let map_proLoca = null;
let gp_layer_projArea = null;
let gp_layer_proLoca = null;

$(window).on("map:init", function (e) {
  //get the map refrence
  var detail = e.originalEvent ? e.originalEvent.detail : e.detail;
  
  if(detail.id == "id_project_area_coordinates-map"){

    map_projArea = detail.map;
    gp_layer_projArea = L.featureGroup().addTo(map_projArea);
 }

 if(detail.id == "id_project_location_coordinates-map"){

  map_proLoca = detail.map;
  gp_layer_proLoca = L.featureGroup().addTo(map_proLoca);
}

});

document.addEventListener("DOMContentLoaded", function () {
  // fix to the base template
  document.querySelectorAll(".tm-bg").forEach((el) => el.remove());
  document.querySelectorAll(".tm-bg-controls-wrapper")[0].remove();

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

  // force to mutiselect to single
  $("#id_mision_name_list").on("click", "option", function (event) {
    // clear the previous layers from group layer
    gp_layer_projArea.clearLayers();
    gp_layer_proLoca.clearLayers();



    if (1 <= $(this).siblings(":selected").length) {
      //$(this).removeAttr("selected");
      $(this).prop("selected", false);
    }

    get_flightdataByGUID(
      "flight",
      $("#id_mision_name_list").find(":selected").val(),
      function (returndata_flight) {
        // Flight level data
        let flight = returndata_flight;
       console.log(flight);

       
       //select project info
       $("#id_project_location_name").val(flight.place_name);
       
       // form Mission Info #####
        $("#id_mision_name").val(flight.name);
        $("#id_flight_datetime").val(flight.flight_date);
        $("#id_flight_altitude").val(flight.max_altitude_agl);
        $("#id_flight_duration").val(flight.duration_seconds);
        
          //Enviromental  Info #####
          $("#id_cloud_cover").val(flight.weather_detail.CC);
          $("#id_humidity").val(flight.weather_detail.H);
          $("#id_air_temperature").val(flight.weather_detail.T);
          $("#id_wind_speed").val(flight.weather_detail.W.split("(")[0]);
          $("#id_wind_direction").val(flight.weather_detail.W.split("(")[1].slice(0, -1));
          $("#id_sun_time").val(flight.sun_time);


        
        


        flight.data_plan_area.forEach((element) => {
          
          let validJson = true;
          element.geometry.forEach(function (c) {
            if (
              isNaN(c[0]) ||
              isNaN(c[1]) ||
              c[0] < -90 ||
              c[0] > 90 ||
              c[1] < -180 ||
              c[1] > 180
            ) {
              validJson = false;
            }
          });
          let el= null;
          if(validJson){

            el = L.polyline(L.GeoJSON.coordsToLatLngs(element.geometry),{color: '#0080FF', weight: 4, opacity: 0.8});
            gp_layer_projArea.addLayer(el);
          }

          if(!validJson){
            el = element.geometry.map(coords => coords.map(coord => coord.reverse()));
            el = L.polyline(el,{color: '#FFFF00', weight: 2, opacity: 0.5});
            console.log(el)
            gp_layer_projArea.addLayer(el);
            
            }



        });
        //###########################
        let tasks_equipment = [];
        flight.equipments.forEach((el) => {
          tasks_equipment.push(
            new Promise((resolve, reject) => {
              get_flightdataByGUID(
                "equipment",
                el,
                function (returndata_equipment) {
                  resolve(returndata_equipment);
                }
              );
            })
          );
        });

        let tasks_drone = [];
        Promise.all(tasks_equipment).then((equipmentList) => {
        console.log(equipmentList);

        $("#sensorInfoList").empty();

          equipmentList.forEach((el) => {
            if (el.drone_guid && el.drone_guid.length > 0) {
              tasks_drone.push(
                new Promise((resolve, reject) => {
                  get_flightdataByGUID(
                    "drone",
                    el.drone_guid,
                    function (returndata_drone) {
                      resolve(returndata_drone);
                    }
                  );
                })
              );
            }
if (el.is_battery == "0"){

$("#sensorInfoList").append(
  `<li class="list-group-item"> <b>Equipment:</b> ${el.equipment_type}   <b>Detail:</b> ${el.name}</li>`
);
}



          });

          Promise.all(tasks_drone).then((droneList) => {
            $("#droneInfoList").empty();

            // get the unique drone by sirial number
            droneList = [
              ...droneList.filter(
                (a, i) =>
                  droneList.findIndex(
                    (s) => a.serial_numner === s.serial_numner
                  ) === i
              ),
            ];

            droneList.forEach((el) => {
              $("#droneInfoList").append(
                `<li class="list-group-item"><b>Drone name:</b> ${el.name}</li>`
              );
              $("#droneInfoList").append(
                `<li class="list-group-item"> <b>Brand:</b> ${el.brand} </h5></li>`
              );
              $("#droneInfoList").append(
                `<li class="list-group-item"> <b>Drone type:</b> ${el.drone_type} </h5></li>`
              );
              $("#droneInfoList").append(
                `<li class="list-group-item"> <b>Model:</b> ${el.model} </h5></li>`
              );
              $("#droneInfoList").append(
                `<li class="list-group-item"> <b>Serial number:</b> ${el.serial_number} </h5></li>`
              );

              $("#droneInfoList").append(
                `<li class="list-group-item" style="background: transparent;"></li>`
              );
            });
          });
        });

        //********************** /
        get_flightdataByGUID(
          "place",
          flight.place_guid,
          function (returndata_place) {
            // Flight level data
            let place = returndata_place;

            gp_layer_proLoca.addLayer(
              new L.marker([place.latitude, place.longitude], {
                icon: droneIcone,
              })
            );
            // L.circleMarker([50.5, 30.5]  ).addTo(map);

          
             sleep(2000).then(() => {
            

            map_proLoca.fitBounds(gp_layer_proLoca.getBounds());
            map_proLoca.zoomOut(18);

            sleep(5000).then(() => {

            map_projArea.fitBounds(gp_layer_projArea.getBounds());
            //map_projArea.zoomIn(1);
          });


             });
            //new L.marker([50.5, 30.5])
            //********************** /
          }
        );
      }
    );
  });

  // update the form value
  const get_flightdataByGUID = (flight, guid, callback) => {
    $.getJSON(
      `${window.location.origin}/api/flight/${flight}/${guid}`,
      function (data) {
        callback(data[0]);
      }
    );
  };

  //initialize the leaflet form contro
  sleep(100).then(() => {
    if (!$(".leaflet-draw-section").hasClass("d-none")) {
      $(".leaflet-draw-section").addClass("d-none");
    }
  });

  $("#smartwizard").on(
    "showStep",
    function (e, anchorObject, currentStepIndex, stepDirection) {
      if (currentStepIndex == 1) {
        // validate the map
        map_projArea.invalidateSize();
      }
    }
  );
});
