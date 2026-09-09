import QtQuick
import org.kde.kirigami as Kirigami

Rectangle {
    id: root
    color: "black"

    property int stage

    onStageChanged: {
        if (stage == 2) {
            introAnimation.running = true
        }
    }

    Image {
        id: noise
        anchors.fill: parent
        source: "images/noise.gif"
        fillMode: Image.PreserveAspectCrop
        opacity: 0.28
        asynchronous: true
    }

    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: "black" }
            GradientStop { position: 0.15; color: "transparent" }
            GradientStop { position: 0.85; color: "transparent" }
            GradientStop { position: 1.0; color: "black" }
        }
    }

    Column {
        id: content
        anchors.centerIn: parent
        opacity: 0
        spacing: Kirigami.Units.largeSpacing

        Text {
            text: "SYSTEM"
            font.family: "Courier New"
            font.bold: true
            font.pixelSize: 32
            font.letterSpacing: 6
            color: "#5eead4"
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            text: "INITIALIZING PLASMA SHELL..."
            font.family: "Courier New"
            font.pixelSize: 10
            font.letterSpacing: 2
            color: "#0d6b60"
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }

    OpacityAnimator {
        id: introAnimation
        running: false
        target: content
        from: 0
        to: 1
        duration: Kirigami.Units.veryLongDuration * 2
        easing.type: Easing.InOutQuad
    }
}
