import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { stringify } from '@angular/compiler/src/util';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

//  constructor() {}
//  seedlots = SEEDLOTS;
  li:any;
  object:any;
  headers:any[] = [];
  values:any[] = [];
  
//  constructor(private seedlotService: SeedlotService) {}

constructor(private http : HttpClient){
}


//  ngOnInit(): void{}
  
//  getSeedlots(): void {
//    this.seedlotService.getSeedlots()
//    	.subscribe(seedlots => this.seedlots = seedlots);
//  }

//  ngOnInit(): void {
//    this.getSeedlots();
//  }
  ngOnInit(): void {
//  this.http.get('http://native-plants-backend.herokuapp.com/')
  this.http.get('https://native-plants-backend.herokuapp.com/q/SELECT farm_name, farm_location, contact_email FROM rev2.farms')
  .subscribe(Response => {
  
  // If response comes hideloader() function is called
  // to hide that loader
  this.object = JSON.parse(JSON.stringify(Response))
  // console.log("obj:", this.object)
  this.headers=this.object.headers;
  this.values = this.object.data
  });
}

update_user(){

}
add_farm(){
  
}
add_nursery(){

}
add_lab(){

}
}