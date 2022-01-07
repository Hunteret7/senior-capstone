import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SeedlotsComponent } from './seedlots.component';

describe('SeedlotsComponent', () => {
  let component: SeedlotsComponent;
  let fixture: ComponentFixture<SeedlotsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SeedlotsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SeedlotsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
