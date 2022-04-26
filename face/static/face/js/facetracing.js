function upload_and_return() {
  // Check if the file is empty or not in valid types
  let video_input = $("#id_video_uploading");
  let pic_input = $("#id_pic_uploading");

  // If empty video
  if (video_input.get(0).files.length == 0) {
    $("#id_invalid_video_modal").modal();
    return;
  }

  let video = video_input.get(0).files[0];

  // If empty picture
  if (pic_input.get(0).files.length == 0) {
    $("#id_invalid_pic_modal").modal();
    return;
  }

  let picture = pic_input.get(0).files[0];

  // Check valid video and picture
  if (!is_video(video['type'])) {
    $("#id_invalid_video_modal").modal();
    return;
  }

  if (!is_image(picture['type'])) {
    $("#id_invalid_pic_modal").modal();
    return;
  }

  // Make an ajax call to the backend
  let formData = new FormData()

  formData.append("csrfmiddlewaretoken", getCSRFToken());
  formData.append("input_video", video);
  formData.append("input_picture", picture);

  // Show the spinner icon
  document.getElementById("id-spinner").hidden=false; // Show the spinner
  document.getElementById("id_upload_btn").hidden=true; // Hide the upload button

  $.ajax({
    url: '/process',
    method: 'POST',
    contentType: false,
    processData: false,
    data: formData,
    success: function(res) {
      document.getElementById("id-spinner").hidden=true; // Hide the spinner
      document.getElementById("id_upload_btn").hidden=false; // Show the upload button
      render_table(res);
    },
    error: function() {
      document.getElementById("id-spinner").hidden=true; // Hide the spinner
      document.getElementById("id_upload_btn").hidden=false; // Show the upload button
      $("#id_fail_modal").modal();
    }
  });
}

function render_table(res) {
  // Show the successful notification
  $("#id_success_modal").modal();
  // Concatenate the displaying html string
  for (var i = 0; i < res.result.length; i++) {
    var ml = res.result[i];
    let add_str = '<tr><th scope="row">' + ml.index + '</th>' +
                  '<td>' + ml.timeslot + '</td>' +
                  '<td><img src="' + ml.image + '" width="200ex"></td></tr>';
    $("#id_result_table").append(add_str);
  }
}


function is_image(filetype) {
  // Check if the file is a valid image
  return filetype.split("/")[0] == 'image';
}

function is_video(filetype) {
  // Check if the file is a valid video
  return filetype.split("/")[0] == 'video';
}

function getCSRFToken() {
  // Get the csrf token of the current page
  let cookies = document.cookie.split(";")
  for (let i = 0; i < cookies.length; i++) {
    let c = cookies[i].trim()
    if (c.startsWith("csrftoken=")) {
      return c.substring("csrftoken=".length, c.length)
    }
  }
  return "unknown";
}