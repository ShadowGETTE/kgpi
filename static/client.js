const datachannel_parameters = {
    "ordered": true
};

// peer connection
let pc = null;

// data channel
let dc = null, dcInterval = null;

function createPeerConnection() {
    const config = {
        sdpSemantics: 'unified-plan'
    };

    config.iceServers = [
        {
            url: 'turn:135.181.243.125:3478?transport=udp',
            username: 'user-1',
            credential: 'pass-1'
        }
    ];
    // config.iceTransportPolicy = "relay";

    pc = new RTCPeerConnection(config);

    // connect video
    pc.addEventListener('track', evt => {
        if (evt.track.kind === 'video')
            document.getElementById('video').srcObject = evt.streams[0];
    });

    return pc;
}

function negotiate() {
    return pc
        .createOffer().then(offer => pc.setLocalDescription(offer)).then(() => {
            // wait for ICE gathering to complete
            return new Promise(resolve => {
                if (pc.iceGatheringState === 'complete') {
                    resolve();
                } else {
                    function checkState() {
                        if (pc.iceGatheringState === 'complete') {
                            pc.removeEventListener('icegatheringstatechange', checkState);
                            resolve();
                        }
                    }

                    pc.addEventListener('icegatheringstatechange', checkState);
                }
            });

        }).then(() => {
            const offer = pc.localDescription;

            return fetch('/api/offer/', {
                body: JSON.stringify({
                    sdp: offer.sdp,
                    type: offer.type
                }),
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'POST'
            });
        }).then(response => response.json()).then(answer => {
            return pc.setRemoteDescription(answer);
        }).catch(e => {
            alert(e);
        });
}

function start() {
    pc = createPeerConnection();

    let time_start = null;

    function current_stamp() {
        if (time_start === null) {
            time_start = new Date().getTime();
            return 0;
        } else {
            return new Date().getTime() - time_start;
        }
    }

    dc = pc.createDataChannel('chat', datachannel_parameters);
    dc.onclose = () => {
        clearInterval(dcInterval);
    };
    dc.onopen = () => {
        dcInterval = setInterval(() => {
            const message = 'ping ' + current_stamp();
            dc.send(message);
        }, 1000);
    };

    const constraints = {
        audio: false,
        video: true
    };

    document.getElementById('media').style.display = 'block';
    navigator.mediaDevices.getUserMedia(constraints).then(stream => {
        stream.getTracks().forEach(track => {
            pc.addTrack(track, stream);
        });
        return negotiate();
    }, err => {
        alert('Could not acquire media: ' + err);
    });
}

function stop() {
    // close data channel
    if (dc) {
        dc.close();
    }

    // close transceivers
    if (pc.getTransceivers) {
        pc.getTransceivers().forEach(transceiver => {
            if (transceiver.stop) {
                transceiver.stop();
            }
        });
    }

    // close local video
    pc.getSenders().forEach(sender => {
        sender.track.stop();
    });

    // close peer connection
    setTimeout(() => {
        pc.close();
    }, 500);
}

start();
