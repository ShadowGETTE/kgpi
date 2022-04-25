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

    // if (document.getElementById('use-stun').checked) {
    config.iceServers = [{urls: ['stun:stun.l.google.com:19302']}];
    // }

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
            let codec;

            codec = document.getElementById('video-codec').value;
            if (codec !== 'default') {
                offer.sdp = sdpFilterCodec('video', codec, offer.sdp);
            }

            return fetch('/api/offer/', {
                body: JSON.stringify({
                    sdp: offer.sdp,
                    type: offer.type,
                    video_transform: 'edges'
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
    document.getElementById('start').style.display = 'none';

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
        video: false
    };

    if (document.getElementById('use-video').checked) {
        let resolution = document.getElementById('video-resolution').value;
        if (resolution) {
            resolution = resolution.split('x');
            constraints.video = {
                // width: parseInt(resolution[0], 0),
                // height: parseInt(resolution[1], 0)
                width: parseInt('1280', 0),
                height: parseInt('720', 0)
            };
        } else {
            constraints.video = true;
        }
    }

    if (constraints.audio || constraints.video) {
        if (constraints.video) {
            document.getElementById('media').style.display = 'block';
        }
        navigator.mediaDevices.getUserMedia(constraints).then(stream => {
            stream.getTracks().forEach(track => {
                pc.addTrack(track, stream);
            });
            return negotiate();
        }, err => {
            alert('Could not acquire media: ' + err);
        });
    } else {
        negotiate();
    }

    document.getElementById('stop').style.display = 'inline-block';
}

function stop() {
    document.getElementById('stop').style.display = 'none';
    document.getElementById('start').style.display = 'inline-block';
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

start(); //autostart
