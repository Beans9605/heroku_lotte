let jcropApi = null;

// @breif 이미지 크롭 영역지정 UI 나타내기
function imgCropDesignate() {
    let editWidth = $("#editImg").width();
    let editHeight = $("#editImg").height();

    // @breif jcrop 실행시 크롭영역을 미리 세팅
    let x1 = window.screen.width / 2 - editWidth;
    let y1 = window.screen.height / 2 - editHeight;
    let x2 = editWidth / 1.5;
    let y2 = editHeight / 1.5;

    // @breif jcrop 실행
    $("#editImg").Jcrop({
          bgFade : true
        , bgOpacity : .2
        , setSelect : [ x1, y1, x2, y2 ]
        , onSelect : updateCoords
    }, function() {
        jcropApi = this;
    });
    $("#editBtn").css("display", "none");
    $("#cutBtn").css("display", "inline");

}

// @breif 지정된 크롭 한 영역( 좌표, 넓이, 높이 )의 값을 보관하는 함수
function updateCoords(crap) {
    $("#xAxis").val(crap.x);
    $("#yAxis").val(crap.y);
    $("#wLength").val(crap.w);
    $("#hLength").val(crap.h);
}

// @breif 크롭한 영역 잘라내고 추출하기
function imgCropApply() {
    if(parseInt($("#wLength").val()) == "NaN") {
        alert("이미지를 크롭한 이후\n자르기 버튼을 클릭하세요.");
    } else {
        let editImage = new Image();
        editImage.src = $("#editImg").attr("src");
        editImage.onload = function() {
            // @breif 캔버스 위에 이미지 그리기
            let canvas = document.querySelector("canvas");
            let canvasContext = canvas.getContext("2d");

            // @breif 캔버스 크기를 이미지 크기와 동일하게 지정
            canvas.width = $("#wLength").val();
            canvas.height = $("#hLength").val();
                 
            canvasContext.drawImage(
                  this
                , $("#xAxis").val()        // 자르기를 시작할 x좌표
                , $("#yAxis").val()        // 자르기를 시작할 y좌표
                , $("#wLength").val()    // 잘라낸 이미지의 넓이
                , $("#hLength").val()    // 잘라낸 이미지의 높이
                , 0                                         // 캔버스에 이미지를 배치할 x좌표
                , 0                                         // 캔버스에 이미지를 배치할 y좌표
                , $("#wLength").val()    // 사용할 이미지의 넓이(이미지 스트레칭 또는 축소)
                , $("#hLength").val()    // 사용할 이미지의 높이(이미지 스트레칭 또는 축소)
            );

            // @breif 편집한 캔버스의 이미지를 화면에 출력한다.
            let dataURI = canvas.toDataURL("image/jpeg");
            $("#editImg").attr("src", dataURI);

            // @breif 이미지의 크기는 자른 이미지와 동일하게 지정
            $("#editImg").css("width", $("#wLength").val());
            $("#editImg").css("height", $("#hLength").val());
        };

        $("#cutBtn").css("display", "none");
        // @details JCROP을 종료한다.
        jcropApi.destroy();
    jcropApi = null;

    }
}



// @breif 이미지 업로드 함수
function uploadImgFilePrinted() {
    // @details 업로드 파일 정보를 받아온다.
    let fileInfo = document.getElementById("exampleFormControlFile1").files[0];
    let reader = new FileReader();

    reader.onload = function() {
        // @details 업로드 이미지 출력
        jQuery("#editImg").attr("src", reader.result);

        // @details 이미지 크기를 제목 영영과 같게 출력
        jQuery("#editImg").css("width", jQuery("h1").width());

        // @details 이미지 업로드 기능 제거, 추가 업로드 방지
        jQuery("#editImg").parent("a").removeAttr("onClick");

        // @details 편집버튼 노출
        jQuery("#editBtn").css("display", "inline");

        canvasDrawImage(function() {
            alert("이미지 업로드가 완료되었습니다.");
        });
    };

    if(fileInfo) {      	
        // @details readAsDataURL을 통해 업로드한 파일의 URL을 읽어 들인다.
        reader.readAsDataURL(fileInfo);
    }
}

// @breif 캔버스 이미지 생성
function canvasDrawImage(callback) {
    let prepImage = new Image();
    prepImage.src = jQuery("#editImg").attr("src");

    prepImage.onload = function() {
        // @details 캔버스 위에 이미지 그리기
        let canvas = document.querySelector("canvas");
        let canvasContext = canvas.getContext("2d");

        canvas.width = jQuery("#editImg").width();
        canvas.height = jQuery("#editImg").height();
        canvasContext.drawImage(this, 0, 0, jQuery("#editImg").width(), jQuery("#editImg").height());

        // @details 캔버스의 이미지
        let dataURI = canvas.toDataURL("image/jpeg");
        jQuery("#editImg").attr("src", dataURI);
        callback();
    };

}
