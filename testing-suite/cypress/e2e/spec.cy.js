describe('Fairytales 4 Kids Website', () => {
  beforeEach(() => {
    cy.visit('/')
  })

  it('should load the homepage successfully', () => {
    cy.get('body').should('be.visible')
    cy.title().should('contain', 'Fairytales')
  })

  it('should have a welcome message', () => {
    cy.get('h1').should('contain', 'Welcome to Fairytales 4 Kids')
    cy.get('.subtitle').should('contain', 'Where magical stories come to life')
  })

  it('should have a link to stories page', () => {
    cy.get('a[href*="stories.html"]').should('exist')
    cy.get('.enter-button').should('contain', 'Read a Good Story')
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