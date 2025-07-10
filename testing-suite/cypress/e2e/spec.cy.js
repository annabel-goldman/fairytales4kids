describe('Fairytales 4 Kids Website', () => {
  beforeEach(() => {
    cy.visit('/')
  })

  it('should load the homepage successfully', () => {
    cy.get('body').should('be.visible')
    cy.title().should('contain', 'Fairytales')
  })

  it('should have navigation elements', () => {
    cy.get('nav').should('exist')
    cy.get('a').should('have.length.greaterThan', 0)
  })

  it('should have story links', () => {
    cy.get('a[href*="stories"]').should('exist')
  })

  it('should be responsive', () => {
    // Test mobile viewport
    cy.viewport(375, 667)
    cy.get('body').should('be.visible')
    
    // Test tablet viewport
    cy.viewport(768, 1024)
    cy.get('body').should('be.visible')
    
    // Test desktop viewport
    cy.viewport(1280, 720)
    cy.get('body').should('be.visible')
  })

  it('should have proper meta tags', () => {
    cy.get('meta[name="viewport"]').should('exist')
    cy.get('meta[charset]').should('exist')
  })
})