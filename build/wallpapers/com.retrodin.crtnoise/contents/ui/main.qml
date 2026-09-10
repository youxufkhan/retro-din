/*
    Animated CRT-noise wallpaper for the Retro DIN theme.

    The lock screen and desktop both load a wallpaper *plugin*, so an animated
    background has to be one - org.kde.image renders a still frame whatever
    you point it at. AnimatedImage is what plays the loop; plain Image decodes
    only the first frame.
*/
import QtQuick
import org.kde.plasma.plasmoid

WallpaperItem {
    id: root

    Rectangle {
        anchors.fill: parent
        color: "#16191a"
    }

    AnimatedImage {
        id: noise
        anchors.fill: parent
        source: Qt.resolvedUrl("../images/noise.gif")
        fillMode: root.configuration.Tiled ? Image.Tile
                                           : Image.PreserveAspectCrop
        opacity: root.configuration.NoiseOpacity
        playing: true
        cache: false
        asynchronous: true
    }

    // vignette, so the panel and greeter controls stay legible over the noise
    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#cc000000" }
            GradientStop { position: 0.35; color: "#00000000" }
            GradientStop { position: 0.65; color: "#00000000" }
            GradientStop { position: 1.0; color: "#cc000000" }
        }
    }
}
