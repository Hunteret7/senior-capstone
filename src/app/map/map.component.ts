import { Component, OnInit } from "@angular/core"
import * as L from "leaflet"

@Component({
  selector: "app-map",
  templateUrl: "./map.component.html",
  styleUrls: ["./map.component.css"],
})
export class MapComponent implements OnInit {
  constructor() {}

  map: any

  ngOnInit(): void {
    this.map = L.map("map").setView([51.505, -0.09], 13)
    this.initMap()
  }

  initMap(): void {
    L.tileLayer(
      "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}",
      {
        maxZoom: 18,
        id: "mapbox/streets-v11",
        tileSize: 512,
        zoomOffset: -1,
        accessToken:
          "pk.eyJ1Ijoiemhlbmd6dW8iLCJhIjoiY2t5bWM5cTk5M2YwbjJ2cGI4cmpwZmhkNCJ9.IzkLw4whcSBVtLpqiE3NYg",
      }
    ).addTo(this.map)
  }

  changeMap(type: String): void {
    let id = "mapbox/streets-v11"
    let url = "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}"
    if (type == "2") {
      id = "mapbox/dark-v10"
    }
    console.log(id)
    L.tileLayer(
      url,
      {
        maxZoom: 18,
        id,
        tileSize: 512,
        zoomOffset: -1,
        accessToken:
          "pk.eyJ1Ijoiemhlbmd6dW8iLCJhIjoiY2t5bWM5cTk5M2YwbjJ2cGI4cmpwZmhkNCJ9.IzkLw4whcSBVtLpqiE3NYg",
      }
    ).addTo(this.map)
  }
}
