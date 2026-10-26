import QtQuick
import "." as P

// Obsidian: retícula de líneas finas sobre negro, selección en blanco invertido. Cuadrícula de 5 columnas.
Item {
    id: st
    property var rows: []
    property int sel: 0
    property string query: ""
    property bool shown: false
    readonly property int cols: 5
    signal picked(int i)
    signal hovered(int i)

    readonly property color paper: "#0B0B0D"
    readonly property color raised: "#101013"
    readonly property color ink: "#E6E6E9"
    readonly property color muted: "#85858D"
    readonly property color line: "#29292E"
    readonly property color brand: "#FFFFFF"

    width: 676
    height: 560
    onSelChanged: grid.positionViewAtIndex(sel, GridView.Contain)

    Rectangle { anchors.fill: parent; anchors.margins: -1; radius: 3; color: st.line }
    Rectangle { anchors.fill: parent; radius: 2; color: st.paper; border.width: 1; border.color: st.line }

    Item {
        id: head
        x: 24; y: 18; width: parent.width - 48; height: 48
        Text {
            id: lab
            text: "01 // BUSCAR"
            color: st.muted
            font.family: "Space Grotesk"; font.pixelSize: 11; font.bold: true; font.letterSpacing: 1
            anchors.verticalCenter: parent.verticalCenter
        }
        Text {
            x: lab.width + 18
            anchors.verticalCenter: parent.verticalCenter
            text: st.query
            color: st.ink
            font.family: "Space Grotesk"; font.pixelSize: 20
            Rectangle {
                x: parent.width + 3; y: 2; width: 10; height: parent.height - 4; color: st.brand
                SequentialAnimation on opacity { running: st.shown; loops: Animation.Infinite
                    NumberAnimation { to: 0; duration: 520 } NumberAnimation { to: 1; duration: 520 } }
            }
        }
        Text {
            anchors.right: parent.right; anchors.verticalCenter: parent.verticalCenter
            text: ("0" + st.rows.length).slice(-2)
            color: st.muted; font.family: "Space Grotesk"; font.pixelSize: 12; font.bold: true
        }
        Rectangle { anchors.bottom: parent.bottom; width: parent.width; height: 1; color: st.ink; opacity: 0.25 }
    }

    GridView {
        id: grid
        x: 18; y: 78; width: parent.width - 36; height: parent.height - 96
        cellWidth: 128; cellHeight: 112
        clip: true
        model: st.rows
        boundsBehavior: Flickable.StopAtBounds
        delegate: Item {
            id: cell
            required property int index
            required property var modelData
            width: grid.cellWidth; height: grid.cellHeight
            readonly property bool on: index === st.sel
            Rectangle {
                anchors.fill: parent; anchors.margins: 6
                radius: 2
                color: cell.on ? st.ink : st.raised
                border.width: 1; border.color: cell.on ? st.ink : st.line
                Behavior on color { ColorAnimation { duration: 120; easing.type: Easing.OutCubic } }
                Column {
                    anchors.centerIn: parent
                    spacing: 6
                    P.AppIcon { anchors.horizontalCenter: parent.horizontalCenter; entry: cell.modelData; size: 48 }
                    Text {
                        width: 104
                        horizontalAlignment: Text.AlignHCenter
                        text: cell.modelData ? cell.modelData.name : ""
                        elide: Text.ElideRight
                        color: cell.on ? "#050505" : st.ink
                        font.family: "Space Grotesk"; font.pixelSize: 11; font.bold: false
                    }
                }
            }
            MouseArea {
                anchors.fill: parent; hoverEnabled: true; cursorShape: Qt.PointingHandCursor
                onPositionChanged: st.hovered(cell.index)
                onClicked: st.picked(cell.index)
            }
        }
    }
}
