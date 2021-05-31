let fileCount = 0;

function getDebugOutputFileList() {
    const urlParams = new URLSearchParams(window.location.search);
    const filename = urlParams.get('filename');
    const index = Number(filename);

    // debug file list get 방식으로 요청
    $.ajax({
        type: 'GET',
        url: 'getDebugOutputFileList',
        dataType: 'JSON',
        success: function (data) {
            // filelist 를 받아옴
            var filelist = data.result2;

            var list = document.getElementById('filelist');

            // 내가 가지고 있는 fileCount와 결과로 받아온 filelist의 length가 다르면
            if (filelist.length !== fileCount) {
                list.innerHTML = '<a class="nav-link" href="/">home</a>'

                if (index >= 1 && index <= fileCount) {
                    if (index != 1) {
                        list.innerHTML += `<a class="nav-link" href="/log-debug?filename=${(index) - 1}">⇑</a>`
                    }
                    if (index != fileCount) {
                        list.innerHTML += `<a class="nav-link" href="/log-debug?filename=${(index) + 1}">⇓</a>`
                    }
                }

                var li;
                var a;
                // filelist 정보 추가
                for (var i = 0; i < filelist.length; i++) {

                    list.innerHTML += `<div class="nav-link" onclick="log_debug_content(${filelist[i]})">${filelist[i]}</div>`
                    // div = document.createElement('div');
                    // div.className="nav-link";

                    // div.innerHTML = `${filelist[i]}`;
                    // list.appendChild(div);
                }
                // fileCount 에 저장하고
                fileCount = filelist.length;
            }
        },
        error: function (request, status, error) {
            alert('통신 실패')
        }
    })

};


function log_debug_content(filename) {
    $.ajax({
        type: 'GET',
        url: 'log-debug-content?filename=' + filename,
        dataType: 'JSON',
        success: function (data) {
            content = data.content

            $("#page").empty();
            for (var i = 0; i < content.length; i++) {
                $("#page").append("<dd>" + content[i] + " </dd>");
            }
        },
        error: function (request, status, error) {
            alert('통신 실패')
        }
    })
}

function saveItToNewfileIfMarked() {
    $.ajax({
        type: 'GET',
        url: 'saveItToNewfileIfMarked',
        dataType: 'JSON',
        success: function (data) {
        },
        error: function (request, status, error) {
            alert('통신 실패')
        }
    })

}

$(document).on('click', '.nav-link', function () {

    var sBtn = $(".nav-link");    //  ul > li 이를 sBtn으로 칭한다. (클릭이벤트는 li에 적용 된다.)
    
    sBtn.removeClass("active");     // sBtn 속에 (active) 클래스를 삭제 한다.
    $(this).addClass("active"); // 클릭한 a에 (active)클래스를 넣는다.

    // sBtn.click(function () {   // sBtn에 속해 있는  a 찾아 클릭 하면.
    //     console.log("click")
    //     sBtn.removeClass("active");     // sBtn 속에 (active) 클래스를 삭제 한다.
    //     $(this).addClass("active"); // 클릭한 a에 (active)클래스를 넣는다.
    // })
});


var timer, timer2;

function init() {
    saveItToNewfileIfMarked();
    getDebugOutputFileList();
    // 최초에 함수를 한번 실행시켜주고 
    timer = setInterval(getDebugOutputFileList, 2000);
    timer2 = setInterval(saveItToNewfileIfMarked, 2000);
    // setInterval이라는 함수로 매초마다 실행을 해줍니다.
    // setInterval은 첫번째 파라메터는 함수이고 두번째는 시간인데 밀리초단위로 받습니다. 1000 = 1초 

}
init();

