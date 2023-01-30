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
let flightGUID = "";

$(window).on("map:init", function (e) {
  //get the map refrence
  var detail = e.originalEvent ? e.originalEvent.detail : e.detail;

  if (detail.id == "id_project_area_coordinates-map") {
    map_projArea = detail.map;
    gp_layer_projArea = L.featureGroup().addTo(map_projArea);
  }

  if (detail.id == "id_project_location_coordinates-map") {
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
    .on("click", (e) => {
      e.preventDefault();

      if (
        !($('input[name="drone_type"]:checked').val() == undefined) &&
        !(flightGUID.length == 0)
      ) {
        $.getJSON(
          `${window.location.origin}/api/ddcregcheck/${flightGUID}`,
          function (data) {
            if (data.response == "not_found") {
              add_dronelogbook_record();
            }
            if (data.response == "found") {
              update_dronelogbook_record();
            }
          }
        ).fail(function (xhr, status, error) {
          console.log("Error: " + status + " - " + error);
        });
      } else {
        $.confirm({
          title:
            '<span class="text-danger"><b>Encountered an error!</b></span>',
          content:
            '<span class="text-dark">Both the field <b>*Flight Mission</b>and <b>*Drone Type</b> must be selected.</span>',
          type: "red",
          typeAnimated: true,
          buttons: {
            tryAgain: {
              text: "Close",
              btnClass: "btn-red",
              action: function () {},
            },
          },
        });
      }
    });

  // gather all parameter for dronelogbook to update or create
  const gatherFormpara_dronlogbook = () => {
    let para = {
      drone_type: $('input[name="drone_type"]:checked').val(),
      flight_mission_guid: flightGUID,
      flight_mission_name: $("#id_mision_name").val(),
      image_overlap: $("#id_image_overlap").val(),
      sensor_dates_last_calibration: $("#id_sensor_info_dates_last_calibration")
        .val()
        .replace(/(\d{2})\/(\d{2})\/(\d{4})/, "$3-$1-$2"),
      sensor_dates_last_maintenance: $("#id_sensor_info_dates_last_maintenance")
        .val()
        .replace(/(\d{2})\/(\d{2})\/(\d{4})/, "$3-$1-$2"),
      secchi_depth: $("#id_secchi_depth").val(),
      turbidity: $("#id_turbidity").val(),
      salinity: $("#id_salinity").val(),
      water_temperature: $("#id_water_temperature").val(),
      cdom: $("#id_cdom").val(),
      //csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    };

    Object.keys(para).forEach(
      (key) => (para[key] == null || para[key] === "") && delete para[key]
    );
    return para;
  };

  const add_dronelogbook_record = () => {
    //####
    $.ajax({
      type: "POST",
      contentType: "application/json",
      url: `/api/ddcreg/`,
      data: JSON.stringify(gatherFormpara_dronlogbook()),
      headers: {
        "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0]
          .value,
      },
      success: function (response) {
        $.confirm({
          title: '<span class="text-success"><b>successful!</b></span>',
          content:
            '<span class="text-dark">Data has been store successfully</span>',
          type: "green",
          typeAnimated: true,
          buttons: {
            tryAgain: {
              text: "Close",
              btnClass: "btn-green",
              action: function () {},
            },
          },
        });
      },
      error: function (jqXHR) {
        console.log(jqXHR);
        $.confirm({
          title: '<span class="text-danger"><b>Unsuccessful!</b></span>',
          content:
            '<span class="text-dark">Error while saving data in database.</span>',
          type: "red",
          typeAnimated: true,
          buttons: {
            tryAgain: {
              text: "Close",
              btnClass: "btn-red",
              action: function () {},
            },
          },
        });
      },
    });
    //###
  };

  const update_dronelogbook_record = () => {
    $.ajax({
      type: "PUT",
      contentType: "application/json",
      url: `/api/ddcreg/${flightGUID}/`,
      data: JSON.stringify(gatherFormpara_dronlogbook()),
      headers: {
        "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0]
          .value,
      },
      success: function (response) {
        $.confirm({
          title: '<span class="text-success"><b>successful!</b></span>',
          content:
            '<span class="text-dark">Data has been updated successfully</span>',
          type: "green",
          typeAnimated: true,
          buttons: {
            tryAgain: {
              text: "Close",
              btnClass: "btn-green",
              action: function () {},
            },
          },
        });
      },
      error: function (jqXHR) {
        console.log(jqXHR);
        $.confirm({
          title: '<span class="text-danger"><b>Unsuccessful!</b></span>',
          content:
            '<span class="text-dark">Error while saving data in database.</span>',
          type: "red",
          typeAnimated: true,
          buttons: {
            tryAgain: {
              text: "Close",
              btnClass: "btn-red",
              action: function () {},
            },
          },
        });
      },
    });
  };

  var btnList = $(
    '<button class= "btn btn-info" value="Input"  type="button"><i class="fas fa-solid  fa-list-ol"></i></button>'
  ).on("click", (e) => {
    e.preventDefault();
    window.location.href = "/ddclist";
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
    $("#smartwizard").smartWizard("loader", "show");

    flightGUID = $("#id_mision_name_list").find(":selected").val();
      
    // tigger to update the dataupload form
    updateDownloadStepEntries();

    $.getJSON(
      `${window.location.origin}/api/ddcregcheck/${flightGUID}`, (event) => {
        data = event.data;
        
        let da_drone_type =
          event.response == "found" && data.drone_type != null ? data : null;


        da_drone_type != null
          ? $(`input[name='drone_type'][value='${data.drone_type}']`).prop(
              "checked",
              true
            )
          : $("input[name='drone_type']").prop("checked", false);

        $("#id_image_overlap").val(
          event.response == "found" && data.image_overlap != null
            ? data.image_overlap
            : null
        );

        $("#id_sensor_info_dates_last_calibration").val(
          event.response == "found" &&
            data.sensor_dates_last_calibration != null
            ? data.sensor_dates_last_calibration.replace(
                /(\d{4})-(\d{2})-(\d{2})/,
                "$2/$3/$1"
              )
            : null
        );

        $("#id_sensor_info_dates_last_maintenance").val(
          event.response == "found" &&
            data.sensor_dates_last_maintenance != null
            ? data.sensor_dates_last_maintenance.replace(
                /(\d{4})-(\d{2})-(\d{2})/,
                "$2/$3/$1"
              )
            : null
        );

        $("#id_secchi_depth").val(
          event.response == "found" && data.secchi_depth != null
            ? data.secchi_depth
            : null
        );

        $("#id_turbidity").val(
          event.response == "found" && data.turbidity != null
            ? data.turbidity
            : null
        );

        $("#id_salinity").val(
          event.response == "found" && data.salinity != null
            ? data.salinity
            : null
        );

        $("#id_water_temperature").val(
          event.response == "found" && data.water_temperature != null
            ? data.water_temperature
            : null
        );

        $("#id_cdom").val(
          event.response == "found" && data.cdom != null ? data.cdom : null
        );
        // map the value from the droneextra para to form
        //$('input[name="drone_type"]:checked').val()
        ///////// to be fix***************************
        //( da != null ? data.dat : null ? $(`input[name='drone_type'][value='${da.drone_type}']`).prop("checked", true) : $(`input[name='${da.drone_type}']`).prop("checked", false));

        // flight_mission_guid: flightGUID,
        // flight_mission_name: $("#id_mision_name").val(),
        // image_overlap: $("#id_image_overlap").val(),
        // sensor_dates_last_calibration: $("#id_sensor_info_dates_last_calibration").val().replace(/(\d{2})\/(\d{2})\/(\d{4})/, "$3-$1-$2"),
        // sensor_dates_last_maintenance: $("#id_sensor_info_dates_last_maintenance").val().replace(/(\d{2})\/(\d{2})\/(\d{4})/, "$3-$1-$2"),
        // secchi_depth: $("#id_secchi_depth").val(),
        // turbidity: $("#id_turbidity").val(),
        // salinity: $("#id_salinity").val(),
        // water_temperature: $("#id_water_temperature").val(),
        // cdom: $("#id_cdom").val(),
        // csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()

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

            //store flight drone
            flightGUID = flight.guid;

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
            $("#id_wind_direction").val(
              flight.weather_detail.W.split("(")[1].slice(0, -1)
            );
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
              let el = null;
              if (validJson) {
                el = L.polyline(L.GeoJSON.coordsToLatLngs(element.geometry), {
                  color: "#0080FF",
                  weight: 4,
                  opacity: 0.8,
                });
                gp_layer_projArea.addLayer(el);
              }

              if (!validJson) {
                el = element.geometry.map((coords) =>
                  coords.map((coord) => coord.reverse())
                );
                el = L.polyline(el, {
                  color: "#FFFF00",
                  weight: 2,
                  opacity: 0.5,
                });
                // console.log(el);
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
              // console.log(equipmentList);

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
                if (el.is_battery == "0") {
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
                  $("#smartwizard").smartWizard("loader", "hide");
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
      }
    ).fail(function (xhr, status, error) {
      console.log("Error: " + status + " - " + error);
    });
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
  let executedmapZoomForm2 = false;
  $("#smartwizard").on(
    "showStep",
    function (e, anchorObject, currentStepIndex, stepDirection) {
      if (currentStepIndex == 1) {
        // validate the map
        map_projArea.invalidateSize();

        // code block to be executed only once
        if (!executedmapZoomForm2) {
          map_projArea.fitBounds(gp_layer_projArea.getBounds());
          console.log("I am in");
          executedmapZoomForm2 = true;
        }
      }
      if (currentStepIndex == 0) {
        // validate the map
        map_proLoca.invalidateSize();
      }
    }
  );

  sleep(1000).then(() => {
    // bootstap date picker take time to configure properly while loading the teh applicatiopn
    $("#id_sensor_info_dates_last_calibration").attr("disabled", true);
    $("#id_sensor_info_dates_last_maintenance").attr("disabled", true);
  });


  // will exicute once when page is loded fully
  let guid = new URLSearchParams(location.search).get("guid");
  if (guid) {
    $("#smartwizard").smartWizard("loader", "show");
    $(`#id_mision_name_list option[value='${guid}']`)
      .prop("selected", true)
      .click();
  }



      



// ###################   window load finish ##########################


});



$(".UploadIcone").on("click", function (ev) {
  let idObj = $(ev.currentTarget)
  .closest("div")
  .find("input.custom-file-input")[0].id;

  $(`#${idObj}`).click()


 
});





$(".edit-icon, .edit-icon-for-calander").on("click", function (ev) {
  let idObj = $(ev.currentTarget)
    .closest("div")
    .find("input.form-control")[0].id;
  $(`#${idObj}`).attr("disabled", !$(`#${idObj}`).attr("disabled"));
  $(ev.currentTarget).toggleClass("text-secondary");
});






$(".edit-icon-for-radio").on("click", function (ev) {
  let idObj = $(ev.currentTarget).closest("div").find(".form-group")[0].id;

  $(ev.currentTarget).toggleClass("text-secondary");

  $(`#${idObj}`)
    .find('input[type="radio"]')
    .attr(
      "disabled",
      $(`#${idObj}`).find('input[type="radio"]').attr("disabled") === "disabled"
        ? false
        : true
    );
});



// upload data to minio
$(".progress").hide();
$("#id_upload_data").click(function() {
  
 
   $(".progress").show();


  $.ajax({
    xhr: function() {
      var xhr = new XMLHttpRequest();
      xhr.upload.onprogress = function(e) {
        var percent = Math.round((e.loaded / e.total) * 100);
        $(".progress-bar").width(percent + "%").text(percent + "%");
      };
      return xhr;
    },
    type: "POST",
    url: "/api/uploadreg/",
    //enctype: "multipart/form-data",
    data: getupload_FormData(),
    headers: {
      "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0]
        .value,
    },
    contentType: false,
    processData: false,
    success: function(data) {
        console.log("Success!");
        $(".progress").fadeOut();
    },
    error: function(error) {
        console.log("Error:", error);
    }
});





});




const getupload_FormData = ()  =>{

  let formData = new FormData();
  formData.append('flight_mission_guid', flightGUID);
  formData.append('mosaiced_image', $('#id_mosaiced_image')[0].files[0] != null? $('#id_mosaiced_image')[0].files[0] :"");
  formData.append('row_image', $('#id_row_image')[0].files[0] != null? $('#id_row_image')[0].files[0] :"");
  formData.append('ground_control_point', $('#id_ground_control_point')[0].files[0] != null? $('#id_ground_control_point')[0].files[0] :"");
  formData.append('ground_truth_point', $('#id_ground_truth_point')[0].files[0] != null? $('#id_ground_truth_point')[0].files[0] :"");
  formData.append('dronePath', $('#id_dronePath')[0].files[0] != null? $('#id_dronePath')[0].files[0] :"");

  return formData;

}



// update the upload step entries

const updateDownloadStepEntries = () =>{


  $.getJSON(
    `${window.location.origin}/api/uploadregcheck/${flightGUID}`,
    function (data) {
      if (data.response == "not_found") {
          //reset_download_record();
      }
      if (data.response == "found") {
       
        update_download_record(data);
      }
    }
  ).fail(function (xhr, status, error) {
    console.log("Error: " + status + " - " + error);
  });


}


const update_download_record = (data) =>{

    let da = Object.entries(data.data).map( ([key,value]) => ({ ["id_"+key]: value } ));


  $("#step-5 label.custom-file-label ").each( (index,el)=> {
    
   
    if( $(el).attr("for") in data)
   
    $(el).text('okkkk ');
   /// to be started
});


  
}








/* 
$.ajax({
  xhr: function() {
      var xhr = new window.XMLHttpRequest();
      xhr.upload.addEventListener("progress", function(evt) {
          if (evt.lengthComputable) {
              var percentComplete = evt.loaded / evt.total;
              percentComplete = parseInt(percentComplete * 100);
              $("#progressbar").width(percentComplete+'%');
              $("#progressbar").html(percentComplete+'%');
          }
      }, false);
      return xhr;
  },
  type: "POST",
  url: "/api/uploadreg/",
  //enctype: "multipart/form-data",
  data: formData,
  headers: {
    "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken")[0]
      .value,
  },
  contentType: false,
  processData: false,
  success: function(data) {
      console.log("Success!");
  },
  error: function(error) {
      console.log("Error:", error);
  }
}); */