// lastno : 현재까지 표시한 파일 포인터 위치를 나타냄 
// 실행할 때는 0 으로 초기화
let lastno = '0';

function getlog() {
    // get 방식으로 lastno를 쿼리 인자를 통해 전달함.
    $.ajax({
        type: 'GET',
        url: 'getlog',
        data: {
            "lastno" : lastno
        },
        dataType: 'JSON',
        success: function (data) {
            //성공적으로 값을 전달 받으면 lastno 이후 정보들을 logresult 저장
            var logresult = data.result2;

            var o = document.getElementById('list');
            var dd;

            // log 정보 추가
            for (var i = 0; i < logresult.length; i++) {
                dd = document.createElement('dd');
                dd.appendChild(document.createTextNode(logresult[i].msg));
                o.appendChild(dd);
            }

            // 가장 아래로 스크롤
            o.scrollTop = o.scrollHeight;
            // lastno를 최신으로 초기화
            lastno = data.lastno;
  
            console.log(lastno);
        },
        error: function (request, status, error) {
            alert('통신 실패')
        }
    })

};

var timer;

function init() {
    getlog();
    // 최초에 함수를 한번 실행시켜주고 
    timer = setInterval(getlog, 1500);
    // setInterval이라는 함수로 매초마다 실행을 해줍니다.
    // setInterval은 첫번째 파라메터는 함수이고 두번째는 시간인데 밀리초단위로 받습니다. 1000 = 1초 
}
init();
