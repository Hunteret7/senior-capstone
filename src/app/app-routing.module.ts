import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SeedlotsComponent } from './seedlots/seedlots.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { MapComponent } from './map/map.component'

const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'seedlots', component: SeedlotsComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'map', component: MapComponent },
  ];

  @NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
 })
 export class AppRoutingModule { }
