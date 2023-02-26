/* globals Chart:false, feather:false */
feather.replace();

function modifyMailing(obj) {
    const mailingModal = $("#mailingModal");
    let modalBody = $('.modal-body');


    $.get($(obj).data('url'), function (data, status) {
        modalBody.html(data);
    });

    mailingModal.modal({show: true});
    $("#saveMailing").data('url', $(obj).data('url'));
}

function saveMailing(obj) {
    let mailingModal = $("#mailingModal");
    let modalBody = $('.modal-body');
    console.log($(obj).data('url'));
    $.ajax({
        url: $(obj).data('url'),
        type: 'post',
        data: $("form").serialize(),
        success: function (data) {
            if (data['success']) {
                mailingModal.modal('hide');
                modalBody.html('');
                getMailingList();
            } else {
                modalBody.html(data);
            }

        }
    });
}

function getMailingList() {
    $.get("/mailings/main/", function (data) {
        $('.table-responsive').html(data);
    });
}

function celeryMailing(obj) {
    $.get($(obj).data('url'), function (data, status) {
        getMailingList();
    });
}


