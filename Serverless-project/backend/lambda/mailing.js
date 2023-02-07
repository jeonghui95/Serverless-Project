var aws = require('aws-sdk');
aws.config.update({region: 'us-west-1'});


exports.handler = (event, context, callback) => {
    // 요청 바디에서 값을 가지고 옵니다.
    
    
    var response = {
        "success" : true
    };
    
    
    var phonenumber = event.Records[0].Sns.Message.split(', ')[3];
    var phonenumber = phonenumber.replace('0','+82')
    response['phone number'] = phonenumber
    
    var params = {
        Message : "정상적으로 "+event.Records[0].Sns.Message.split(', ')[1]+ " 강의가 등록 되었습니다",
        PhoneNumber: phonenumber
    };
    

   var publishTextPromise = new aws.SNS({ apiVersion: '2010-03-31',region: 'us-west-1'}).publish(params).promise();

    // SDK를 실행합니다.
    publishTextPromise.then(
        function(data) {
            //메세지가 있다면 첫번째에 null, 두번째에 메세지를 리턴합니다.
            console.log('success sdk')
            console.log('PhoneNumber : '+ phonenumber)
            callback(null,"MessageID is " + data.MessageId);
        }).catch(
        function(err) {
			  //에러가 있다면 err를 리턴합니다.
            console.log('error sdk')
            callback(err);
    });
    
    return response
};


    

	