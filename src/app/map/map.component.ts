import { Component, OnInit } from "@angular/core"
import * as L from "leaflet"
@Component({
  selector: "app-map",
  templateUrl: "./map.component.html",
  styleUrls: ["./map.component.css"],
})
export class MapComponent implements OnInit {
  constructor() {}

  ngOnInit(): void {
    this.initMap()
  }

  initMap(): void {
    let map = L.map("map").setView([51.505, -0.09], 13)

    L.tileLayer(
      "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}",
      {
        attribution:
          'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: "mapbox/streets-v11",
        tileSize: 512,
        zoomOffset: -1,
        accessToken:
          "pk.eyJ1Ijoiemhlbmd6dW8iLCJhIjoiY2t5bWM5cTk5M2YwbjJ2cGI4cmpwZmhkNCJ9.IzkLw4whcSBVtLpqiE3NYg",
      }
    ).addTo(map)
  }
}
