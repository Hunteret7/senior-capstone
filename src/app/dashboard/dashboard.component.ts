import { Component, OnInit } from '@angular/core';
import { Seedlot } from '../seedlot';
import { SeedlotService } from '../seedlot.service';

@Component({
    selector: 'app-dashboard',
    templateUrl: './dashboard.component.html',
    styleUrls: [ './dashboard.component.css' ]
  })
  export class DashboardComponent implements OnInit {
    seedlots: Seedlot[] = [];

  constructor(private seedlotService: SeedlotService) { }

  ngOnInit(): void {
    this.getSeedlots();
  }

  getSeedlots(): void {
    this.seedlotService.getSeedlots()
      .subscribe(seedlots => this.seedlots = 
        seedlots.slice(1, 5));
  }
}
