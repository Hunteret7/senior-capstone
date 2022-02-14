import { Component, OnInit } from '@angular/core';
import { Seedlot } from '../seedlot';
//import {SEEDLOTS} from '../mock-seedlots';
import { SeedlotService } from '../seedlot.service';
import { HttpClient } from '@angular/common/http';
import { stringify } from '@angular/compiler/src/util';

@Component({
  selector: 'app-seedlots',
  templateUrl: './seedlots.component.html',
  styleUrls: ['./seedlots.component.css']
})

export class SeedlotsComponent implements OnInit {
//  constructor() {}
//  seedlots = SEEDLOTS;
  seedlots: Seedlot[] = [];
  li:any;
  object:any;
  headers:any[] = [];
  values:any[] = [];
//  constructor(private seedlotService: SeedlotService) {}

constructor(private http : HttpClient){
}

  selectedSeedlot?: Seedlot;
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
  this.http.get('https://native-plants-backend.herokuapp.com/q/SELECT user_name, name, user_role_type as admin_level, email FROM rev2.users')
  .subscribe(Response => {
  
  // If response comes hideloader() function is called
  // to hide that loader
  this.object = JSON.parse(JSON.stringify(Response))
  // console.log("obj:", this.object)
  this.headers=this.object.headers;
  this.values = this.object.data
  });
}

onSelect(seedlot : Seedlot): void{
  	this.selectedSeedlot = seedlot;
	}
}

