import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { FormsModule } from '@angular/forms'; // NgModel lives here
import { AppComponent } from './app.component';
import { SeedlotsComponent } from './seedlots/seedlots.component';
import { AppRoutingModule } from './app-routing.module';
import { DashboardComponent } from './dashboard/dashboard.component';
import { FarmsComponent } from './farms/farms.component';
import { NursuriesComponent } from './nursuries/nursuries.component';
import { ProfileComponent } from './profile/profile.component';

@NgModule({
  declarations: [
    AppComponent,
    SeedlotsComponent,
    DashboardComponent,
    FarmsComponent,
    NursuriesComponent,
    ProfileComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
