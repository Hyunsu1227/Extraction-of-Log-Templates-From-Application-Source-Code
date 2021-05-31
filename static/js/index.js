$(document).ready(function () {
    // 문서의 로딩을 시작할때
    // log 리스트 불러오기
    $.ajax({
        type: 'GET',
        url: '/loglist',
        dataType: 'JSON',
        success: function (data) {
            $("#item_category").html("")
            console.log("here")
            // loglist 를 받아 웹에 표시
            // log name 으로 정렬하면 좋을듯 front 에서 할지 서버에서 할지
            var logllist = data.result2;
            for (var k = 0; k < logllist.length; k++) {
                $("#item_category").append('<option value ="' + logllist[k] + '">' + logllist[k] + '</option>');
            }
        },
        error: function (request, status, error) {
            alert('통신 실패')
        }
    })

    $.ajax({
        type: 'GET',
        url: '/getLogFileList',
        dataType: 'JSON',
        success: function (data) {
            console.log('success')
            var filenamelist = data.result2;
            for (var k = 0; k < filenamelist.length; k++) {
                $("#result-file-list").append('<input type="checkbox" name="check" value="'+filenamelist[k]+'" id="rd2"/><span style = "cursor:pointer;" onclick = "window.open(\'log?filename='+encodeURI(filenamelist[k])+'\')"> '+filenamelist[k]+'</span><br>');
            }

        },
        error: function (request, status, error) {
            alert('통신 실패')
        }
    })

    $.ajax({
        type: 'GET',
        url: '/getDebugFileList',
        dataType: 'JSON',
        success: function (data) {
            console.log('success')
            var filenamelist = data.result2;
            for (var k = 0; k < filenamelist.length; k++) {
                $("#result-debug-file-list").append('<input type="checkbox" name="check" value="'+filenamelist[k]+'" id="rd2"/><span style = "cursor:pointer;" onclick = "window.open(\'log-debug?debug-file='+encodeURI(filenamelist[k])+'\')"> '+filenamelist[k]+'</span><br>');
            }

        },
        error: function (request, status, error) {
            alert('통신 실패')
        }
    })
    
});

// id 가 excute 인 버튼을 클릭 시 
$(document).on('click', '#execute', function () {
    // 입력받은 log file name 과 debug_mode 가 True 인지 False 인지 저장함.
    log_name = $('#item_category').val();
    debug_mode = $('input:checkbox[id="debug-mode"]').is(":checked");

    // post data 에 json 형태로 저장
    var postdata = {
        'log_name': log_name, 'debug_mode': debug_mode
    }
    console.log(postdata)
    // /excute 에 post 전달
    $.ajax({
        type: 'POST',
        url: '/excute',
        data: JSON.stringify(postdata),
        dataType: 'JSON',
        contentType: "application/json",
        success: function (data) {
            if(debug_mode == false){
                filename = data.result2
                // /log 로 이동함.
                location.href = "/log?filename=" + filename
            } else{
                filename = data.result2
                // /log 로 이동함.
                location.href = "/log-debug?debug-file=" + filename
            }
            
        },
        error: function (request, status, error) {
            alert('ajax 통신 실패')
            alert(error);
        }
    })
});

$(document).on('click', '#delete', function () {
    var filenames=[]; 
    $('input[name="check"]:checkbox:checked').each(function()
    {
        filenames.push($(this).val());
    }); 
    if(filenames.length == 0)
    {
        alert("항목을 선택해주세요")
    }
    else{
        var postdata = {
            'filename':filenames
        }       
        $.ajax({
            type: 'POST',
            url: 'deletefile',
            data: JSON.stringify(postdata),
            dataType : 'JSON',
            contentType: "application/json",
            success: function(data){
                location.reload();
            }
        });
    }

});

function moveWebPage(filename)
{ 
    location.href = "/log?filename=" + filename
}



