import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NursuriesComponent } from './nursuries.component';

describe('NursuriesComponent', () => {
  let component: NursuriesComponent;
  let fixture: ComponentFixture<NursuriesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NursuriesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NursuriesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
