import { Injectable } from '@angular/core';
import { Seedlot } from './seedlot';
import { SEEDLOTS } from './mock-seedlots';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class SeedlotService {
  
  getSeedlots(): Observable<Seedlot[]> {
    const seedlots = of(SEEDLOTS);
    return seedlots;
  }

  constructor() { }
}
