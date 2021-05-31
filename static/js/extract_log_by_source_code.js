$(document).ready(function () {
    // 문서의 로딩을 시작할때
    // log 리스트 불러오기
    getUploadFileList()
});

$(document).on('click', '#allselect', function () {
    const $container = document.querySelector('#upload-file-list');
    const $inputs = [...$container.children];

    if ($inputs.filter(input => input.checked).length === $inputs.length) {
        $inputs.forEach(input => { input.checked = false; });
    } else {
        $inputs.forEach(input => {
            input.checked = true;
        });
    }
});

$(document).on('click', '#delete', function () {
    var filenames = [];
    $('input[name="check"]:checkbox:checked').each(function () {
        filenames.push($(this).val());
    });
    if (filenames.length == 0) {
        alert("항목을 선택해주세요")
    }
    else {
        var postdata = {
            'filename': filenames
        }
        $.ajax({
            type: 'POST',
            url: 'deletefile',
            data: JSON.stringify(postdata),
            dataType: 'JSON',
            contentType: "application/json",
            success: function (data) {
                // location.reload();
                getUploadFileList()
            }
        });
    }

});

function getUploadFileList() {
    $.ajax({
        type: 'GET',
        url: '/getUploadFileList',
        dataType: 'JSON',
        success: function (data) {
            console.log('success')
            var filenamelist = data.result2;
            $("#upload-file-list").empty()
            for (var k = 0; k < filenamelist.length; k++) {
                $("#upload-file-list").append('<input type="checkbox" name="check" value="' + filenamelist[k] + '" id="rd2"/>' + " " + filenamelist[k] + '<br>');
            }

        },
        error: function (request, status, error) {
            alert('통신 실패')
        }
    })
}

// id 가 excute 인 버튼을 클릭 시 
$(document).on('click', '#execute', function () {
    var filenames = [];
    var extension_type = $('#extension_type').val();
    $('input[name="check"]:checkbox:checked').each(function () {
        filenames.push($(this).val());
    });
    if (filenames.length == 0) {
        alert("항목을 선택해주세요")
    }
    else {
        var postdata = {
            'filename': filenames,
            'extension_type': extension_type
        }
        $.ajax({
            type: 'POST',
            url: 'excute_extract_log_by_source_code',
            data: JSON.stringify(postdata),
            dataType: 'JSON',
            contentType: "application/json",
            success: function (data) {
                success = data.result2
                fail = data.result3
                loglist = data.result4
                stat = data.result5

                $("#table").empty()
                // $("#loglist").empty()
                // $("#success").empty()
                $("#fail").empty()

                $("#table").append(
                    `<table border="1">
                    <th>num_log</th>
                    <th>success</th>
                    <th>fail</th>
                    <tr><!-- 첫번째 줄 시작 -->
                        <td>${stat['num_log']}</td>
                        <td>${stat['success']}</td>
                        <td>${stat['fail']}</td>
                    </tr><!-- 첫번째 줄 끝 -->
                </table>
                <br>
                <table border="1">
                    <th>type</th>
                    <th>count</th>
                    <tr><!-- 첫번째 줄 시작 -->
                        <td>var_only</td>
                        <td>${stat['var_only']}</td>
                    </tr>
                    <tr>
                        <td>string_no_var</td>   
                        <td>${stat['string_no_var']}</td>
                    </tr>
                    <tr>
                        <td>string_var_1</td>
                        <td>${stat['string_var_1']}</td>
                    </tr>
                    <tr>
                        <td>string_var_over_2</td>
                        <td>${stat['string_var_over_2']}</td>
                    </tr>
                    <tr>
                        <td>string_with_e</td>
                        <td>${stat['string_with_e']}</td>
                    </tr> 
                    <tr>
                        <td>classification_failure</td>
                        <td>${stat['classification_failure']}</td>
                    </tr><!-- 첫번째 줄 끝 -->
                </table>
                `

                )
                $("#loglist > p").remove("#data");
                $("#loglist").prepend('<p id="data">LOG LIST <br></p>');
                // $("#loglist").append('<textarea id="text_loglist" name="story" rows="20" cols="100" wrap="off" >' + loglist + '</textarea>');
                $("textarea#text_loglist").val(loglist);

                $("#success > p").remove("#data");
                $("#success").prepend('<p id="data">SUCCESS <br></p>');
                // $("#success").append('<textarea id="text_success" name="story" rows="20" cols="100" wrap="off" >' + success + '</textarea>');
                $("textarea#text_success").val(success);

                $("#fail").append('<p id="data">FAIL <br></p>');
                $("#fail").append('<textarea id="story" name="story" rows="20" cols="100" wrap="off" >' + fail + '</textarea>');
                
            }
        });
    }
});

// id 가 excute 인 버튼을 클릭 시 
$(document).on('click', '#viewFileContent', function () {
    var filenames = [];
    $('input[name="check"]:checkbox:checked').each(function () {
        filenames.push($(this).val());
    });
    if (filenames.length == 0) {
        alert("항목을 선택해주세요")
    }
    else {
        var url = "";

        for (var k = 0; k < filenames.length; k++) {

            url = "/sourcecode?filename=";
            url += filenames[k];
            
            window.open(url, filenames[k] + String(k));
        }
    }
});

var $divs = $('#text_loglist, #text_success');
var sync = function(e){
    var $other = $divs.not(this).off('scroll'), other = $other.get(0);
    var percentage = this.scrollTop / (this.scrollHeight - this.offsetHeight);
    other.scrollTop = percentage * (other.scrollHeight - other.offsetHeight);
    setTimeout( function(){ $other.on('scroll', sync ); },10);
}
$divs.on( 'scroll', sync);