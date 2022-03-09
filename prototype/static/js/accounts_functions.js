function show(currentdivId, anotherdiv1, anotherdiv2, currentTab, otherTab1, otherTab2) {
    $("#" + anotherdiv1).hide();
    $("#" + anotherdiv2).hide();
    $("#" + currentdivId).show();
    $('#' + currentTab).css({ "border-bottom": "3px solid #0600a6" });
    $('#' + otherTab1).css({ "border": "none" });
    $('#' + otherTab2).css({ "border": "none" });
}

$(document).on('submit', '#profile_pic_form', function (e) {
    e.preventDefault();
    var form_data = new FormData($(this)[0]);
    $.ajax({
        type: 'POST',
        url: '/upload/',
        processData: false,
        contentType: false,
        data: form_data,
        success: function (response) {
            $("#profile_pic_div").load(location.href + " #profile_pic_div");
        }
    });
});


function showprofilepicuploadarea(divid) {
    $("#" + divid).show();
}
function savedatatodatabase(formid, url, nextdivId, anotherdiv1, anotherdiv2, currentTab, otherTab1, otherTab2) {
    $(document).on('submit', formid, function (e) {
        e.preventDefault();
        var form_data = new FormData($(this)[0]);

        $.ajax({
            type: 'POST',
            url: url,
            processData: false,
            contentType: false,
            data: form_data,
            success: function (response) {
                $("#profile_pic_div").load(location.href + " #profile_pic_div");
                $("#" + anotherdiv1).hide();
                $("#" + anotherdiv2).hide();
                $("#" + nextdivId).show();
                $('#' + currentTab).css({ "border-bottom": "3px solid #0600a6" });
                $('#' + otherTab1).css({ "border": "none" });
                $('#' + otherTab2).css({ "border": "none" });

            }
        });
    });
}
function validateImage(fileid) {
    var fname = document.getElementById(fileid).value;
    var re = /(\.jpg|\.jpeg|\.bmp|\.gif|\.png)$/i;
    if (!re.exec(fname)) {
        document.getElementById(fileid).value = "";
        alert("File extension not supported!");

    }
}
function validateFile(fileid) {
    var fname = document.getElementById(fileid).value;
    var re = /(\.pdf|\.pptx)$/i;
    if (!re.exec(fname)) {
        document.getElementById(fileid).value = "";
        alert("File extension not supported!");

    }
}
function check(id, input1, input2) {
    if (document.getElementById(id).checked) {
        document.getElementById(input1).readOnly = false;
        document.getElementById(input2).readOnly = false;

    } else {
        document.getElementById(input1).readOnly = true;
        document.getElementById(input2).readOnly = true;
    }
}

function submitData(formid, URL, message) {
    let confirmation = "Are you sure\nEither OK or Cancel.";
    if (confirm(confirmation) == true) {
        $(document).on('submit', formid, function (e) {
            e.preventDefault();
            var form_data = new FormData($(this)[0]);
            $.ajax({
                type: 'POST',
                url: URL,
                processData: false,
                contentType: false,
                data: form_data,
                success: function (response) {
                    $(formid)[0].reset();
                    alert(message);
                    location.reload();

                }
            });
        });
    }

}
function addData(formid, URL, message) {
    $(document).on('submit', formid, function (e) {
        e.preventDefault();
        var form_data = new FormData($(this)[0]);
        $.ajax({
            type: 'POST',
            url: URL,
            processData: false,
            contentType: false,
            data: form_data,
            success: function (response) {
                $(formid)[0].reset();
                alert(message)

            }
        });
    });

}
function viewRow(divId) {

    $(divId).show();
}

function updateDataBase()
    {
        
        let confirmation = "Are you sure\nEither OK or Cancel.";
        if (confirm(confirmation) == true) 
            return true;
        else
            return false;

    }
var delay = 500;
    $(".progress-bar").each(function (i) {
        $(this).delay(delay * i).animate({ width: $(this).attr('aria-valuenow') + '%' }, delay);

        $(this).prop('Counter', 0).animate({
            Counter: $(this).text()
        }, {
            duration: delay,
            easing: 'swing',
            step: function (now) {
                $(this).text(Math.ceil(now) + '%');
            }
        });
    });

function updateWithoutReload(formid,URL){
    $(document).on('submit', formid, function (e) {
        e.preventDefault();
        var form_data = new FormData($(this)[0]);
        $.ajax({
            type: 'POST',
            url: URL,
            processData: false,
            contentType: false,
            data: form_data,
            success: function (response) {
                $(formid)[0].reset();

            }
        });
    });
}