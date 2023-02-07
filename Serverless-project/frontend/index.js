$(document).ready(function(){
    var ENDPOINT = 'https://0j60duw6i7.execute-api.us-west-1.amazonaws.com/develop/lecture'
    // var CF = 'https://d2tzclwaxl28qn.cloudfront.net'
    var dialog = document.querySelector('.print_dialog');
    var dialog_detail = document.querySelector('.detail_dialog');
    var showModalButton = $('.show-modal');
    var lecture_dict = {'msaCloud':'MSA Cloud', 'bigData': 'Big Data', 'IoT':'IoT'}

    // ENDPOINT 연결
    if (! dialog.showModal) {
        dialogPolyfill.registerDialog(dialog);
    }

    if(! dialog_detail.showModal){
        dialogPolyfill.registerDialog(dialog_detail);
    }

    // show-modal (데이터 qr 코드 보기 : 프린트 버튼 눌렀을 시)
    $(document).on('click', '.show-modal', function(e) {
        e.preventDefault();
        var student_id = $(this).data('student');
        var lecture_name = $(this).data('lecture');
        var path = './qrcodes/'
        var path = path + student_id + '/'
        var path = path + lecture_name + '/'
        var path = path + 'qrcode.jpg'
        
        $('#showBox').html('<img style="width:100%" src="'+path+'"/>');
        console.log(path)
        dialog.showModal();
    });
    dialog.querySelector('.close').addEventListener('click', function() {
        dialog.close();
    });
    dialog.querySelector('.print').addEventListener('click', function() {
        print();
    });

    // detail-modal (데이터 상세 보기 : 파일 모양 눌렀을 시)
    $(document).on('click', '.detail-modal', function(e) {
        e.preventDefault();
        var student_id = $(this).data('student');
        var lecture_name = $(this).data('lecture');
        console.log(student_id)

        var url = ENDPOINT +'/student/'+student_id+'?lecture_name='+lecture_name
        

        // ajax get 시작
        $.ajax({
            url: ENDPOINT +'/student/'+student_id+'?lecture_name='+lecture_name,
            method: 'get',
            success: function(r){
                var get_data = JSON.parse(r['items'])[0]
                console.log(get_data)
                $('input[id=student_id_detail]').prop('value',get_data['student_id']);
                $('input[id=student_name_detail]').prop('value',get_data['student_name']);
                $('input[id=student_phone_detail]').prop('value',get_data['student_phone']);
                $('input[id=student_email_detail]').prop('value',get_data['student_email']);
                $('select[id=lecture_name_detail]').val(get_data['lecture_name']).prop("selected", true);

                $('input[id=student_id_detail]').prop('readonly',true);
                $('select[id=lecture_name_detail]').prop('disabled', true);

            },
            fail: function(err){
                console.log('failed', err);
            },
            complete: function(r){
                console.log('completed', r);
            }
        }); //ajax get 끝

        dialog_detail.showModal();
    });

    dialog_detail.querySelector('.close').addEventListener('click', function() {
        dialog_detail.close();
    });

    // delete-modal (데이터 삭제 : x버튼 눌렀을 시)
    $(document).on('click', '.delete-modal', function(e){
        e.preventDefault();
        var student_id = $(this).data('student');
        var lecture_name = $(this).data('lecture');
        console.log(student_id)

        var confirm_val = confirm("정말 삭제하시겠습니까? 삭제 하시는 경우 복구가 불가합니다.")
        // 삭제 시작
        if (confirm_val){
            $.ajax({
                url: ENDPOINT + '/student',
                method: 'post',
                datatype: 'json',
                async: true,
                data:JSON.stringify({
                    lecture_name: lecture_name,
                    student_id: student_id
                }),
                beforeSend: function(){
                },
                success: function(r){
                    console.log('success', r);
                },
                fail: function(err){
                    console.log('failed', err);
                    alert('failed! reloading...')
                },
                complete: function(r){
                    console.log('completed', r);
                    setTimeout(function() {
                        location.reload();
                    }, 1000);
                }
            }); //AJAX
        } // 삭제 끝
    });


    // 데이터 불러오기
    function load_data(){
        $.ajax({
            url: ENDPOINT +'/student/*',
            method: 'get',
            success: function(r){
                var html = '';
                html += '<ul class="demo-list-three mdl-list mdl-cell mdl-cell--4-col">'
                JSON.parse(r['items']).forEach(function(item) {
                    html += '<li class="mdl-list__item mdl-list__item--three-line"> <span class="mdl-list__item-primary-content"> <i class="material-icons mdl-list__item-avatar">person</i> <span>'
                    html += item['student_id']
                    html += '</span> <span class="mdl-list__item-text-body">'
                    html += 'From. ' + item['lecture_name'] +'<br/> '+item['student_name']
                    html += '</span> </span> <span class="mdl-list__item-secondary-content"> <a data-student="'+item['student_id']+'" data-lecture="'+item['lecture_name']+'" class="show-modal mdl-list__item-secondary-action" href="#"><i class="material-icons">print</i></a> </span>'
                    html += '</span> </span> <span class="mdl-list__item-secondary-content"> <a data-student="'+item['student_id']+'" data-lecture="'+item['lecture_name']+'" class="detail-modal mdl-list__item-secondary-action" href="#"><i class="material-icons">file_open</i></a></span>'
                    html += '</span> </span> <span class="mdl-list__item-secondary-content"> <a data-student="'+item['student_id']+'" data-lecture="'+item['lecture_name']+'" class="delete-modal mdl-list__item-secondary-action" href="#"><i class="material-icons">close</i></a></span>'
                    html += '</li>'
                })
                html += '</ul>'
                $('#history').html(html);
            },
            fail: function(err){
                console.log('failed', err);
            },
            complete: function(r){
                console.log('completed', r);
            }
        });
    }

    // 데이터 수정
    $('#update').on('click', function(e){
        var student_id = $('#student_id_detail').val();
        var lecture_name = $('#lecture_name_detail').val();
        var student_name = $('#student_name_detail').val();
        var student_phone = $('#student_phone_detail').val();
        var student_email = $('#student_email_detail').val();

        var confirm_val = confirm("정말 수정하시겠습니까? 수정 하시는 경우 복구가 불가합니다.")

        if(confirm_val){
            $.ajax({
                url: ENDPOINT +'/student',
                method: 'put',
                datatype: 'json',
                async: true,
                data:JSON.stringify({
                    lecture_name: lecture_name,
                    student_id: student_id,
                    student_name: student_name,
                    student_phone: student_phone,
                    student_email: student_email
                }),
                contentType:'application/json;charset=UTF-8',
                beforeSend: function(){
                    $('#p2').show();
                },
                success: function(r){
                    console.log('success', r);
                },
                fail: function(err){
                    console.log('failed', err);
                    alert('failed! reloading...')
                },
                complete: function(r){
                    console.log('completed', r);
                    setTimeout(function() {
                        $('#p2').hide();
                        alert('수정 완료되었습니다')
                        load_data();
                    }, 1000);
                }
            }); //AJAX
        }
    });
    
    // 데이터 삽입
    $('#submitButton').on('click', function(e){
        var student_id = $('#student_id').val();
        var lecture_name = $('#lecture_name').val();
        var student_name = $('#student_name').val();
        var student_phone = $('#student_phone').val();
        var student_email = $('#student_email').val();

        $.ajax({
            url: ENDPOINT,
            method: 'post',
            datatype: 'json',
            async: true,
            data:JSON.stringify({
                lecture_name: lecture_name,
                student_id: student_id,
                student_name: student_name,
                student_phone: student_phone,
                student_email: student_email
            }),
            beforeSend: function(){
                $('#p2').show();
            },
            success: function(r){
                console.log('success', r);
            },
            fail: function(err){
                console.log('failed', err);
                alert('failed! reloading...')
            },
            complete: function(r){
                console.log('completed', r);
                setTimeout(function() {
                    $('#p2').hide();
                    location.reload();
                }, 1000);
            }
        }); //AJAX

    });

    load_data();
})
