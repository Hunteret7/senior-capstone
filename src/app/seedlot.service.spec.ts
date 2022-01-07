import { TestBed } from '@angular/core/testing';

import { SeedlotService } from './seedlot.service';

describe('SeedlotService', () => {
  let service: SeedlotService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SeedlotService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
