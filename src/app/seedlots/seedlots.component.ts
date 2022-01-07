import { Component, OnInit } from '@angular/core';
import {Seedlot} from '../seedlot';
//import {SEEDLOTS} from '../mock-seedlots';
import { SeedlotService } from '../seedlot.service';

@Component({
  selector: 'app-seedlots',
  templateUrl: './seedlots.component.html',
  styleUrls: ['./seedlots.component.css']
})

export class SeedlotsComponent implements OnInit {
//  constructor() {}
//  seedlots = SEEDLOTS;
  seedlots: Seedlot[] = [];
  constructor(private seedlotService: SeedlotService) {}
  selectedSeedlot?: Seedlot;
//  ngOnInit(): void{}
  
  getSeedlots(): void {
    this.seedlotService.getSeedlots()
    	.subscribe(seedlots => this.seedlots = seedlots);
  }

  ngOnInit(): void {
    this.getSeedlots();
  }

  onSelect(seedlot : Seedlot): void{
  	this.selectedSeedlot = seedlot;
	}
}

