import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SeedlotsComponent } from './seedlots/seedlots.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { FarmsComponent } from './farms/farms.component';
import { NursuriesComponent } from './nursuries/nursuries.component';
import { ProfileComponent } from './profile/profile.component';

const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'seedlots', component: SeedlotsComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'farms', component: FarmsComponent },
  { path: 'nursuries', component: NursuriesComponent },
  { path: 'profile', component: ProfileComponent }
  ];

  @NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
 })
 export class AppRoutingModule { }
