/******************************************************************************
 * HTML5 Multiple File Uploader Demo                                          *
 ******************************************************************************/

// Constants
var MAX_UPLOAD_FILE_SIZE = 1024*1024; // 1 MB
var UPLOAD_URL = "/account";
// var NEXT_URL   = "/account";

// List of pending files to handle when the Upload button is finally clicked.
var PENDING_FILES  = [];


$(document).ready(function() {
    // Set up the drag/drop zone.
    initDropbox();

    // Set up the handler for the file input box.
    $("#file-picker").on("change", function() {
        handleFiles(this.files);
    });

    // Handle the submit button.
    $("#upload-button").on("click", function(e) {
        // If the user has JS disabled, none of this code is running but the
        // file multi-upload input box should still work. In this case they'll
        // just POST to the upload endpoint directly. However, with JS we'll do
        // the POST using ajax and then redirect them ourself when done.
        e.preventDefault();
        doUpload();
    })
});

$("#upload").on("change", function(e) {
    var $dropbox = $("#dropbox");

    // fire the upload here
    e.preventDefault();
    $(this).removeClass("active");

    $dropbox.on("",function(e) {
        console.log('entrou')
        // Get the files.
        var files = e.originalEvent.dataTransfer.files;
        handleFiles(files);
        console.log(files)
        // Update the display to acknowledge the number of pending files.
        $dropbox.text(PENDING_FILES.length + " files ready for upload!");
        // $(this).addClass("dropped");
        doUpload();
        $(this).addClass("dropped");
    });

});


function readURL(input) {
    if (input.files && input.files[0]) {
  
      var reader = new FileReader();
  
      reader.onload = function(e) {

        handleFiles(input.files);
        console.log(input.files)
        doUpload();
        $(this).addClass("dropped");
        //

      };
  
      reader.readAsDataURL(input.files[0]);
    //   input = null;
    } else {
      removeUpload();
    }
  }
  
  function removeUpload() {
    $('.file-upload-input').replaceWith($('.file-upload-input').clone());
    $('.file-upload-content').hide();
    $('.image-upload-wrap').show();
  }
  $('.image-upload-wrap').bind('dragover', function () {
          $('.image-upload-wrap').addClass('image-dropping');
      });
      $('.image-upload-wrap').bind('dragleave', function () {
          $('.image-upload-wrap').removeClass('image-dropping');
  });


function doUpload() {
    
    
    // On drop...
    // $dropbox.on("drop", function(e) {
        // e.preventDefault();
        // $(this).removeClass("active");
    // });

    $("#progress").show();
    var $progressBar   = $("#progress-bar");

    // Gray out the form.
    // $("#upload-form :input").attr("disabled", "disabled");

    // Initialize the progress bar.
    // $progressBar.css({"width": "0%"});

    // Collect the form data.
    fd = collectFormData();

    // Attach the files.
    for (var i = 0, ie = PENDING_FILES.length; i < ie; i++) {
        // Collect the other form data.
        fd.append("file", PENDING_FILES[i]);
    }

    // Inform the back-end that we're doing this over ajax.
    fd.append("__ajax", "true");

    var xhr = $.ajax({

        // url: UPLOAD_URL,
        url: UPLOAD_URL,
        method: "POST",
        contentType: false,
        processData: false,
        cache: false,
        data: fd,
        success: function(data) {
            // location.reload(forceGet=true)
            var $dropbox = $("#dropbox");
            console.log('Entrou')
            console.log(fd.get("file").name)
            document.getElementById("file-upload-success").textContent=fd.get("file").name + " uploaded";
            document.getElementById("file-upload-success").removeAttribute("hidden");
            // $success_span();
            // $success_span.hidden = false;
            
            $dropbox.removeClass("active");
            $dropbox.removeClass("dropped");
            $dropbox.text("Drag and Drop Files Here");
            
            // fd=null;
            // $("#upload").trigger("reset");
            PENDING_FILES  = [];
            // document.getElementById("upload").reset();
            var uuid = data.msg;
            
        },
    }).done(function(data){                 // ; Return JSON da função, e recebe o JSON na variavel data. altera atributo usando a KEY
        console.log(data)
        $('#account-picture').attr('src', data['src']);
    });  

}

function collectFormData() {
    // Go through all the form fields and collect their names/values.
    var fd = new FormData();

    $("#upload-form :input").each(function() {
        var $this = $(this);
        var name  = $this.attr("name");
        var type  = $this.attr("type") || "";
        var value = $this.val();

        // No name = no care.
        if (name === undefined) {
            return;
        }

        // Skip the file upload box for now.
        if (type === "file") {
            return;
        }

        // Checkboxes? Only add their value if they're checked.
        if (type === "checkbox" || type === "radio") {
            if (!$this.is(":checked")) {
                return;
            }
        }

        fd.append(name, value);
    });

    return fd;
}


function handleFiles(files) {
    // Add them to the pending files list.
    // for (var i = 0, ie = files.length; i < ie; i++) {
    if (files.length > 1) {
        alert("Only the first selected file will be uploaded")
    }
    PENDING_FILES.push(files[0]);
    // }
}

$(function(){
    $("#dropbox").on('click', function(e){
        console.log('click')
        e.preventDefault();
        $("#upload").trigger('click');
    });
});


function initDropbox() {
    var $dropbox = $("#dropbox");

    // On mouse over...
    $dropbox.on("mouseover", function(e) {
        e.stopPropagation();
        e.preventDefault();
        $dropbox.text("Click to upload a new picture");
        $(this).addClass("active");
    });

    // On mouse out...
    $dropbox.on("mouseout", function(e) {
        e.stopPropagation();
        e.preventDefault();
        $dropbox.text("Drag and Drop Files Here");
        $(this).removeClass("active");
    });

    // On drag enter...
    $dropbox.on("dragenter", function(e) {
        e.stopPropagation();
        e.preventDefault();
        $(this).addClass("active");
    });

    // On drag over...
    $dropbox.on("dragover", function(e) {
        e.stopPropagation();
        e.preventDefault();
    });

    // On drag leave...
    $dropbox.on("dragleave", function(e) {
        e.stopPropagation();
        e.preventDefault();
        $(this).removeClass("active");
        // $(this).removeClass("dropped");
    });

    // On drop...
    $dropbox.on("drop", function(e) {
        e.preventDefault();
        $(this).removeClass("active");

        // Get the files.
        var files = e.originalEvent.dataTransfer.files;
        handleFiles(files);
        console.log(files)
        // Update the display to acknowledge the number of pending files.
        $dropbox.text(PENDING_FILES.length + " files ready for upload!");
        // $(this).addClass("dropped");
        doUpload();
        $(this).addClass("dropped");
    });


    // If the files are dropped outside of the drop zone, the browser will
    // redirect to show the files in the window. To avoid that we can prevent
    // the 'drop' event on the document.
    function stopDefault(e) {
        e.stopPropagation();
        e.preventDefault();
    }
    $(document).on("dragenter", stopDefault);
    $(document).on("dragover", stopDefault);
    $(document).on("dragleave", stopDefault);
    $(document).on("drop", stopDefault);
}